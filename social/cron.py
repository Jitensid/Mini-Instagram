from django.contrib.auth.models import User
from users.models import Profile
from django.core.mail import send_mail
from django.conf import settings
import datetime 

def wish_bday():

	all_users = Profile.objects.all()
	subject = 'Happy Birthday'
	email_from = settings.EMAIL_HOST_USER

	today = datetime.datetime.now()

	today_day = today.day
	today_month = today.month

	for profile_user in all_users:
		
		if today_day == profile_user.birthdate.day and today_month == profile_user.birthdate.month:
			recipient_list = []
			recipient_list.append((str(profile_user.user.email)))
			message = 'Hello ' + profile_user.user.username + 'Wishing you many many happy returns of the day'
			send_mail( subject, message, email_from, recipient_list)
			
	return True