from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.base import ContentFile
# Create your models here.

class Social(models.Model):
	caption = models.TextField(blank=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)#if a user is deleted than we delete all the posts made by that user
	posted_image = models.ImageField(upload_to='images/', blank=False)
	liked_by = models.ManyToManyField(User, blank=True, related_name = "+")
	no_of_likes = models.PositiveIntegerField(default=0, blank=True)

class MessageBody(models.Model):
	time_for_message = models.DateTimeField(default=timezone.now)
	sender = models.ForeignKey(User,on_delete = models.CASCADE)
	content = models.TextField(blank=False)

class ChatRoom(models.Model):
	room_name = models.TextField(blank=False)
	message_list = models.ManyToManyField(MessageBody)

	def __str__(self):
		return f'{self.room_name}'