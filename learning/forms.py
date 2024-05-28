#TODO: Check entered words against dictionary words for validity.
#TODO: Add words to specified deck
import difflib
import random

import numpy as np
from django import forms
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from .models import Deck, DeckWord
from languages.models import Language, Word
from user_management.models import UserProfile



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

    def save(self, commit=False):
        """
        Saves the form instance.

        Args:
            commit (bool): Whether to commit the save immediately.

        Returns:
            Deck: The saved Deck instance.
        """
        deck = super().save(commit=False)

        if commit:
            deck.save()
            self.save_m2m()

            cleaned_data = self.cleaned_data
            word_items = cleaned_data.get('word_items')

            with transaction.atomic():
                try:
                    for rank, word_item in enumerate(word_items, start=1):
                        deck_entry, created = DeckWord.objects.get_or_create(
                            deck=deck,
                            word_item=word_item,
                            defaults={'rank':1}
                        )
                except IntegrityError as e:
                    raise
        return deck

    class Meta:
        model = Deck
        fields = ['name', 'description', 'is_ranked']

