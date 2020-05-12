from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Following, Follower

@receiver(post_save, sender=User)	#attached a receiver which listens to a signal generated when a user account is created and calls the following function
def create_profile(sender, instance, created, **kwargs): #kwargs = extra argumnets to a function
	if created:									#when user is created 
		# Profile.objects.create(user=instance)	#then the profile of the user is already created
		Follower.objects.create(current_user=instance)
		Following.objects.create(current_user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	# instance.profile.save()
	instance.follower.save()
	instance.following.save()
