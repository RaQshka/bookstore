import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from BookStore.models import Chat, Message, Notification, User, ChatParticipant


class ChatConsumer(AsyncWebsocketConsumer):
    active_users = {}  # Словарь для отслеживания активных пользователей по chat_id

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        user = self.scope['user']

        if not user.is_authenticated:
            await self.close()
            return

        is_participant = await database_sync_to_async(ChatParticipant.objects.filter)(
            chat_id=self.chat_id, user=user
        )
        if not await database_sync_to_async(is_participant.exists)():
            await self.close()
            return

        if self.chat_id not in self.active_users:
            self.active_users[self.chat_id] = set()
        self.active_users[self.chat_id].add(user.id)

        await self.channel_layer.group_add(
            f'user_{user.id}',
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']
        if self.chat_id in self.active_users:
            self.active_users[self.chat_id].discard(user.id)
            if not self.active_users[self.chat_id]:
                del self.active_users[self.chat_id]

        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            f'user_{user.id}',
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json['message']
            user = self.scope['user']

            if not message_text.strip():
                return

            # Предварительная загрузка связанного объекта 'listing'
            chat = await database_sync_to_async(Chat.objects.select_related('listing').get)(id=self.chat_id)
            message = await database_sync_to_async(Message.objects.create)(
                chat=chat,
                sender=user,
                text=message_text
            )

            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'sender': user.username,
                    'sent_at': message.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

            participants = await database_sync_to_async(list)(
                ChatParticipant.objects.filter(chat=chat).exclude(user=user).select_related('user')
            )
            active_user_ids = self.active_users.get(self.chat_id, set())
            for participant in participants:
                if participant.user.id not in active_user_ids:
                    await database_sync_to_async(Notification.objects.create)(
                        user=participant.user,
                        message=message
                    )
                    group_name = f'user_{participant.user.id}'
                    await self.channel_layer.group_send(
                        group_name,
                        {
                            'type': 'send_notification',
                            'message': f'Новое сообщение от {user.username} в чате "{chat.listing.title}"',
                            'chat_id': chat.id,
                        }
                    )
        except Exception as e:
            await self.send(text_data=json.dumps({'error': f'Ошибка: {str(e)}'}))
            print(f"Chat consumer WebSocket error: {str(e)}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sent_at': event['sent_at'],
        }))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'chat_id': event['chat_id'],
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            self.group_name = f'user_{user.id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))