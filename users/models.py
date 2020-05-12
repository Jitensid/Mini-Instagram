from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
# Create your models here.

class Profile(models.Model): #this model inherits from models.Model 
	user = models.OneToOneField(User, on_delete=models.CASCADE)		#this model has an one to one field relation with the User Model provided by Django!!!
	image = models.ImageField(default='default.png', upload_to='media/')	#CASCADE implies that if user is deleted then we remove the profile pic and not vice versa!!!
	bio_for_profile = models.TextField(blank=True)
	birthdate = models.DateField(blank=False)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self,*args,**kwargs): #overriding sae method to resize image
		super(Profile, self).save(*args, **kwargs) #executing save method of the parent 

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Following(models.Model):
	current_user = models.OneToOneField(User, on_delete=models.CASCADE)
	following_to = models.ManyToManyField(User,blank=True, related_name='+')
	no_of_following = models.PositiveIntegerField(default=0);

	def __str__(self):
		return f'{self.current_user.username} Following'

class Follower(models.Model):
	current_user = models.OneToOneField(User, on_delete=models.CASCADE)
	followed_by = models.ManyToManyField(User,blank=True, related_name='+')
	no_of_followers = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f'{self.current_user.username} Follower'