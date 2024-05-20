#TODO: Check entered words against dictionary words for validity.
#TODO: Add words to specified deck
import difflib

from django import forms
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from .models import UserDeck, Deck
from user_management.models import UserProfile
from languages.models import Word


class UserDeckEntryForm(forms.ModelForm):
    word_list_raw = forms.CharField(label='Word list (comma separated)', widget=forms.Textarea(attrs={'rows':5}))
    rank = forms.DecimalField(label='Rank', min_value=0.0, max_value=1.0)

    # Clean word list and enter items into array split at comma
    def clean_word_list(self):
        word_list = self.cleaned_data['word_list_raw']
        word_list = [word.strip() for word in word_list.split(',') if word.strip()]
        return word_list

    def clean(self):
        cleaned_data = super().clean()
        user_profile = cleaned_data.get('user_profile')
        deck = cleaned_data.get('deck')

        if user_profile and deck:
            if not UserDeck.objects.filter(deck=deck, user_profile=user_profile):
                raise forms.ValidationError(f'User {user_profile} does not have edit permissions for this deck.')

        return cleaned_data

    class Meta:
        model = UserDeck
        fields = ['user_profile', 'deck', 'rank']
    # For each word:
        # If word exists in main db:
            # Enter new deck entry
        # Else:
            # Ask for correction
    # Save deck

# class UserDeckAdminForm(forms.ModelForm):
#     username = forms.ModelChoiceField(
#         queryset=User.objects.all(),
#         label='Username',
#         required=True
#     )
#     word_items = forms.CharField(
#         label='Word Items (comma-separated)',
#         widget=forms.Textarea(attrs={'rows': 5}),
#         required=True
#     )
#     active = forms.BooleanField(
#         label='Active',
#         required=False
#     )
#
#     class Meta:
#         model = UserDeck
#         fields = ['deck', 'username', 'active', 'rank']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         user = cleaned_data.get('username')
#         word_items_raw = cleaned_data.get('word_items')
#         deck = cleaned_data.get('deck')
#
#         # Validate the user
#         if not user:
#             raise ValidationError("User is required.")
#
#         cleaned_data['user_profile'] = user.userprofile
#
#         # Validate and match words
#         if deck and word_items_raw:
#             language = deck.language
#             main_word_list = Word.objects.filter(language=language)
#             word_items_list = [word.strip() for word in word_items_raw.split(',') if word.strip()]
#
#             deck_word_list = []
#             for word in word_items_list:
#                 word_match = difflib.get_close_matches(word, [word_obj.value for word_obj in main_word_list], n=1)
#                 if word_match:
#                     base_word = main_word_list.get(value=word_match[0])
#                     deck_word_list.append(base_word)
#                 else:
#                     raise ValidationError(f"Word '{word}' does not exist in the '{language}' language.")
#
#             cleaned_data['word_items'] = deck_word_list
#
#         return cleaned_data
#
#     @transaction.atomic
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#
#         # Use the cleaned data to get the user_profile and word_items
#         user_profile = self.cleaned_data['user_profile']
#         word_items = self.cleaned_data['word_items']
#         active = self.cleaned_data['active']
#         rank = self.cleaned_data['rank']
#         deck = self.cleaned_data['deck']
#
#         print(word_items)
#
#         # Save each word item to UserDeck
#         for word_item in word_items:
#             UserDeck.objects.create(
#                 deck=deck,
#                 user_profile=user_profile,
#                 word_item=word_item,
#                 rank=rank,
#                 active=active
#             )
#
#         # if commit:
#         #     instance.save()
#         # return instance