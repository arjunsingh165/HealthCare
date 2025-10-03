import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.room_group_name = f'chat_{self.chat_room_id}'
        
        # Check if user is authenticated
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return
        
        # Check if user is participant in this chat room
        is_participant = await self.is_chat_participant(user, self.chat_room_id)
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'chat_message')
        
        if message_type == 'chat_message':
            message = text_data_json['message']
            sender = self.scope["user"]
            
            # Save message to database
            message_obj = await self.save_message(
                chat_room_id=self.chat_room_id,
                sender=sender,
                content=message
            )
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender.id,
                    'sender_name': sender.full_name,
                    'sender_role': sender.role,
                    'timestamp': message_obj.timestamp.isoformat(),
                    'message_id': message_obj.id,
                }
            )
        elif message_type == 'mark_read':
            # Mark messages as read
            await self.mark_messages_read(self.chat_room_id, self.scope["user"])

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'sender_role': event['sender_role'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def is_chat_participant(self, user, chat_room_id):
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            return user in [chat_room.patient, chat_room.doctor] or user.role == 'admin'
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, chat_room_id, sender, content):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        message = Message.objects.create(
            chat_room=chat_room,
            sender=sender,
            content=content,
            message_type='text'
        )
        return message

    @database_sync_to_async
    def mark_messages_read(self, chat_room_id, user):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        Message.objects.filter(
            chat_room=chat_room,
            is_read=False
        ).exclude(sender=user).update(is_read=True)
