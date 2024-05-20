import difflib

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline

from languages.models import Word
from .models import Deck, UserDeck, SystemDeck, UserWordBank, UserSentence, UserWordDeck, UserWordBuffer, FrequencyWordDeck

from .forms import UserDeckEntryForm

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

# class UserDeckAdmin(admin.ModelAdmin):
#     list_display = ['user_profile', 'deck', 'word_item', 'rank']

class UserWordBufferInline(GenericTabularInline):
    model = UserWordBuffer

@admin.register(UserWordBuffer)
class UserWordBufferAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'language', 'deck_source', 'object_id', 'priority', 'word_item', 'proficiency', 'fail_pass_ratio', 'date_modified']
    search_fields = ['user_profile__username', 'language__name', 'content_type__model']
    list_filter = ['user_profile', 'language', 'deck_source']
    ordering = ['-priority']

class UserDeckAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'deck', 'word_item', 'rank']
    form = UserDeckEntryForm
    def save_model(self, request, obj, form, change):
        if form.is_valid():
            user_profile = form.cleaned_data['user_profile']
            deck = form.cleaned_data['deck']

            word_list = form.cleaned_data['word_list_raw'].split(',')
            rank = form.cleaned_data['rank']

            language = deck.language
            main_word_list = Word.objects.filter(language=language)

            for word in word_list:
                word_match = difflib.get_close_matches(word, [word_obj.value for word_obj in main_word_list], n=1)
                if word_match:
                    word_item = main_word_list.get(value=word_match[0])
                    print(word_item)
                    UserDeck.objects.create(
                        deck=deck,
                        user_profile=user_profile,
                        word_item=word_item,
                        rank=rank,
                        active=True
                    )
    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

admin.site.register(UserDeck,UserDeckAdmin)