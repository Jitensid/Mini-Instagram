from .models import ChatRoom, MessageBody, User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender = ChatRoom)
def delete_chatroom(sender, instance, **kwargs):

    message_list = instance.message_list.all()

    for messages in message_list:
        messages.delete()

    

