import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from BookStore.models import Chat, Message, Notification, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

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
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        user = self.scope['user']

        # Save message to database
        chat = await database_sync_to_async(Chat.objects.get)(id=self.chat_id)
        message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            sender=user,
            text=message_text
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': user.username,
                'sent_at': message.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

        # Create notifications for other participants
        participants = await database_sync_to_async(list)(chat.chatparticipant_set.exclude(user=user))
        for participant in participants:
            await database_sync_to_async(Notification.objects.create)(
                user=participant.user,
                message=message
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sent_at': event['sent_at'],
        }))