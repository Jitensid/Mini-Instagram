from django.contrib import admin
from .models import Social, ChatRoom, MessageBody


# Register your models here.

admin.site.register(Social)
admin.site.register(MessageBody)
admin.site.register(ChatRoom)