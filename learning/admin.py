from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import UserWordBank, UserSentence, UserWordDeck, UserWordBuffer, FrequencyWordDeck

admin.site.register(UserSentence)
admin.site.register(UserWordBank)
admin.site.register(UserWordDeck)
# admin.site.register(UserWordBuffer)
# admin.site.register(FrequencyWordDeck)

@admin.register(FrequencyWordDeck)
class UserWordDeckAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'word_item', 'frequency_rating')

class UserWordBufferInline(GenericTabularInline):
    model = UserWordBuffer

@admin.register(UserWordBuffer)
class UserWordBufferAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'language', 'content_type', 'object_id', 'priority', 'word_item']
    search_fields = ['user_profile__username', 'language__name', 'content_type__model']
    list_filter = ['user_profile', 'language', 'content_type']