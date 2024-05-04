from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Deck, SystemDeck, UserWordBank, UserSentence, UserWordDeck, UserWordBuffer, FrequencyWordDeck

admin.site.register(UserSentence)
admin.site.register(UserWordBank)
admin.site.register(UserWordDeck)
# admin.site.register(UserWordBuffer)
# admin.site.register(FrequencyWordDeck)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'language', 'visibility']


@admin.register(SystemDeck)
class SystemDeckAdmin(admin.ModelAdmin):
    list_display = ['deck', 'word_item', 'rank']

class UserWordBufferInline(GenericTabularInline):
    model = UserWordBuffer

@admin.register(UserWordBuffer)
class UserWordBufferAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'language', 'deck_type', 'object_id', 'priority', 'word_item']
    search_fields = ['user_profile__username', 'language__name', 'content_type__model']
    list_filter = ['user_profile', 'language', 'deck_type']