from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Deck, UserDeck, SystemDeck, UserWordBank, UserSentence, UserWordDeck, UserWordBuffer, FrequencyWordDeck

from .forms import UserDeckAdminForm

admin.site.register(UserSentence)
admin.site.register(UserWordBank)
# admin.site.register(UserWordDeck)
# admin.site.register(UserWordBuffer)
# admin.site.register(FrequencyWordDeck)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'language', 'visibility']


@admin.register(SystemDeck)
class SystemDeckAdmin(admin.ModelAdmin):
    list_display = ['deck', 'word_item', 'rank']

class UserWordBufferInline(GenericTabularInline):
    model = UserWordBuffer

@admin.register(UserWordBuffer)
class UserWordBufferAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'language', 'deck_source', 'object_id', 'priority', 'word_item', 'proficiency', 'fail_pass_ratio', 'date_modified']
    search_fields = ['user_profile__username', 'language__name', 'content_type__model']
    list_filter = ['user_profile', 'language', 'deck_source']
    ordering = ['-priority']

class UserDeckAdmin(admin.ModelAdmin):
    list_display = ['deck', 'word_item', 'rank']

admin.site.register(UserDeck, UserDeckAdmin)