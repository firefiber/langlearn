from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserLanguageProficiency
from django.contrib.auth.forms import UserCreationForm

# class UserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
#
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('native_language', 'learning_languages')  # add other fields if necessary
#
# # a user creation form that will also create a user profile, with the user's native language and learning languages
# class UserAndProfileForm(UserCreationForm):

# a user creation form that will create a user account and a user profile for that same account. it will ask for the username, email, password, native language, and learning language. when submitted, it will create a user account and a user profile for that same account. the user profile will have the native language and learning language that the user specified.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_management.models import UserProfile, Language
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    @transaction.atomic
    def save(self):
        user = super().save()
        user.email = self.cleaned_data.get('email')
        user.save()

        try:
            native_language = Language.objects.get(name='English')
            learning_language = Language.objects.get(name='Spanish')
        except ObjectDoesNotExist:
            # Handle the error if the language does not exist
            return user

        user_profile = UserProfile.objects.create(user=user,
                                                  native_language=native_language)

        user_profile.learning_languages.add(
            learning_language, through_defaults={'is_active': True}
        )

        return user


