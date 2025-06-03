import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from BookStore.models import Chat, Message, Notification, User, ChatParticipant

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        user = self.scope['user']

        if not user.is_authenticated:
            await self.close()
            return

        is_participant = database_sync_to_async(ChatParticipant.objects.filter)(
            chat_id=self.chat_id, user=user
        )
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json['message']
            user = self.scope['user']

            if not message_text.strip():
                return

            chat = await database_sync_to_async(Chat.objects.get)(id=self.chat_id)
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

            # Fetch participants asynchronously
            participants = await database_sync_to_async(list)(
                ChatParticipant.objects.filter(chat=chat).exclude(user=user).select_related('user')
            )
            for participant in participants:
                await database_sync_to_async(Notification.objects.create)(
                    user=participant.user,
                    message=message
                )
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
            await self.close()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sent_at': event['sent_at'],
        }))