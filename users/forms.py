from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from bootstrap_datepicker_plus import DatePickerInput

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'special'})) #default value of the validator is true which is sufficent for many purposes
	class Meta:#gives us space for configurations for a specific model
		model = User #name of the model which would get affected  so form.save would save the data in the User model
		fields = ['username', 'email', 'password1', 'password2']#order of the fields which needs to be shown in the form


	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

class UserUpdateForm(forms.ModelForm):  #this form inherits from forms.ModelForm

		class Meta:
			model = User
			fields = ['username']

		def __init__(self, *args, **kwargs):
			super(UserUpdateForm, self).__init__(*args, **kwargs)
			for fieldname in ['username']:
				self.fields[fieldname].help_text = None

class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		fields = ['image', 'bio_for_profile']

		model = Profile

class BirthDayForm(forms.Form):
    birthdate = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )