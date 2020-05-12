from django import forms
from django.contrib.auth.models import User
from .models import Social 



class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Social
		fields = ['caption', 'posted_image']