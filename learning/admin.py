import difflib

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

from languages.models import Word
from .models import Deck, DeckWord, UserWordBank, UserWordBuffer, UserDeckSubscription, UserDeckBufferWord
from .forms import DeckCreateForm, UserDeckSubscriptionForm

admin.site.register(UserWordBank)


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'language', 'is_ranked', 'created_by', 'visibility']
    form = DeckCreateForm


@admin.register(UserDeckSubscription)
class UserDeckSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'deck', 'is_active', 'created']
    form = UserDeckSubscriptionForm

@admin.register(DeckWord)
class DeckWordAdmin(admin.ModelAdmin):
    list_display = ['deck', 'word_item', 'rank']
    ordering = ['rank']

@admin.register(UserWordBuffer)
class UserWordBufferAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'deck', 'deck_length', 'is_fully_loaded']

@admin.register(UserDeckBufferWord)
class UserDeckBufferWordAdmin(admin.ModelAdmin):
    list_display = ['buffer', 'word_item', 'priority', 'proficiency']

