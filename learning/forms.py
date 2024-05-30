import difflib
import random

from django import forms
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Deck, DeckWord, UserDeckSubscription, UserWordBuffer, UserDeckBufferWord
from languages.models import Language, Word
from user_management.models import UserProfile

import numpy as np


class DeckCreateForm(forms.ModelForm):
    """
    A form for creating and validating a Deck instance.
    """
    input_word_items = forms.CharField(
        label='Word list (comma separated)',
        widget=forms.Textarea(attrs={'rows':5})
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.filter(category='L'),
        label='Language'
    )
    created_by = forms.ModelChoiceField(
        queryset=UserProfile.objects.all(),
        label='Username'
    )

    def clean(self):
        """
        Cleans and validates the form data.

        Returns:
            dict: The cleaned data.

        Raises:
            ValidationError: If any word in the input_word_items does not exist in the database.
        """
        cleaned_data = super().clean()

        language = cleaned_data.get('language')
        word_items_raw = cleaned_data.get('input_word_items')
        word_items_raw = [word.strip() for word in word_items_raw.split(',') if word.strip()]

        word_items = []
        for word_item in word_items_raw:
            try:
                word = Word.objects.get(language=language,value=word_item)
                word_items.append(word)
            except Word.DoesNotExist:
                raise ValidationError('Word not found')
        cleaned_data['word_items'] = word_items
        return cleaned_data

    def save(self, commit=True):
        deck = super().save(commit=False)

        deck.save()
        self.save_m2m()

        cleaned_data = self.cleaned_data
        word_items = cleaned_data.get('word_items')

        with transaction.atomic():
            try:
                for rank, word_item in enumerate(word_items, start=1):
                    deck_word_entry = DeckWord.objects.get_or_create(
                        deck=deck,
                        word_item=word_item,
                        defaults={'rank':rank}
                    )
            except IntegrityError as e:
                raise e
        
        return deck

    class Meta:
        model = Deck
        fields = ['name', 'description', 'is_ranked']

# TODO: Make subscription form so that subscribing to a deck immediately creates a buffer for that deck.
class UserDeckSubscriptionForm(forms.ModelForm):

    def save(self, commit=True):
        subscription = super().save(commit=False)

        subscription.save()
        self.save_m2m()

        deck = subscription.deck
        deck_items = DeckWord.objects.filter(deck=deck).order_by('rank')
        deck_length = deck_items.count()

        user_profile = subscription.user_profile

        with transaction.atomic():
            buffer = UserWordBuffer.objects.create(
                user_profile=user_profile,
                deck=deck,
                deck_length=deck_length,
            )

            buffer.refill_buffer()

        return subscription

    class Meta:
        model = UserDeckSubscription
        fields = ['user_profile', 'deck', 'is_active']