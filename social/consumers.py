from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import MessageBody, ChatRoom
from django.contrib.auth.models import User
from datetime import datetime

class ChatCustomer(WebsocketConsumer):
        
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        chat_room = self.scope["url_route"]["kwargs"]["room_name"]

        current_chat_room = ChatRoom.objects.get(room_name = chat_room)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

        for messages in current_chat_room.message_list.all():

            self.send(text_data=json.dumps({
                'message': messages.content,
                'sender' : messages.sender.username,
                'date' :  messages.time_for_message.strftime("%d-%m-%Y %H:%M"),
            }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        
        message = text_data_json['message']
        
        sender = text_data_json['sender']

        date = datetime.now().strftime("%d-%m-%Y %H:%M")

        sender_user = User.objects.get(username = sender)

        new_message = MessageBody(sender=sender_user,content = message, time_for_message = datetime.now())

        new_message.save()

        chat_room = self.scope["url_route"]["kwargs"]["room_name"]

        current_chat_room = ChatRoom.objects.get(room_name = chat_room)

        current_chat_room.message_list.add(new_message)

        current_chat_room.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender' : sender,
                'date' : date,
            }
        )

    # Receive message from room group
    def chat_message(self, event):

        message = event['message']
        sender = event['sender']
        date = event['date']

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender' : sender,
            'date' : date,
        }))