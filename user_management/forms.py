from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserLanguageProficiency
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('native_language',)  # add other fields if necessary
