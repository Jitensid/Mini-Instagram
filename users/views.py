from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, BirthDayForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.conf import settings
from .models import Following, Follower, Profile
from django.template import RequestContext
from social.models import Social
from django.contrib.auth.models import User
import urllib
import json

# Create your views here.
@ensure_csrf_cookie # a decorator for csrf token
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)#create a form which has a method POST
		b_form = BirthDayForm(request.POST)
		if form.is_valid() and b_form.is_valid():

			recaptcha_response = request.POST.get("g-recaptcha-response")
			url = 'https://www.google.com/recaptcha/api/siteverify'

			values = {
				'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response' : recaptcha_response
			}
          
			data = urllib.parse.urlencode(values).encode()

			req = urllib.request.Request(url, data=data)

			response = urllib.request.urlopen(req)

			result = json.loads(response.read().decode())


			if result["success"]:

				form.save()#thats it for adding the user into the database!!!!

				username = form.cleaned_data.get('username')#grabs username from the data entered into the form
			
				date = b_form.cleaned_data.get('birthdate') #grabs date from the form 
				
				new_user = User.objects.get(username=username)

				new_profile = Profile(user=new_user,birthdate=date)
				new_profile.save()

				messages.success(request, f'Account created for {username}!!')
				subject = 'Thank You for registering to our website'
				message = 'It means a world to us '
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [form.cleaned_data.get('email')]  #fetching the email from form and greeting the user with an email
				send_mail( subject, message, email_from, recipient_list)
				return redirect('login')

			else:
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')

	else:
		form = UserRegisterForm()
		b_form = BirthDayForm()
		#created an instance of the inbuilt usercreation form
	return render(request, 'users/final_register.html', {'form': form, 'b_form' : b_form}) #passed the form into html page register.html


@login_required #view will be executed if and only if a user is logged in the system
def profile(request): #creating a profile page for every user
	following_users = Following.objects.get(current_user=request.user)
	follower_users = Follower.objects.get(current_user=request.user)
	posted_images = Social.objects.filter(author=request.user).order_by("-date_posted")
	return render(request, 'users/final_profile.html',{'following_users': following_users.no_of_following, 'follower_users':follower_users.no_of_followers, 'no_of_posts':posted_images.count,'posted_images': posted_images})	

def edit_profile(request):

	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST,instance=request.user)
		profile_update_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

		if user_form.is_valid() and profile_update_form.is_valid():
			user_form.save()
			profile_update_form.save()
			return redirect('profile')

	else:
		user_form = UserUpdateForm(instance=request.user)#filling data of the form from previous data stored in the dataBase
		profile_update_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'user_form' : user_form,
		'profile_update_form': profile_update_form
	}

	return render(request, 'users/profupdate.html', context)