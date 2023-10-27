# from django import forms
# from django.contrib import admin
# from .models import Sentence
# from .services import store_sentence
#
# admin.site.register(Language)
# admin.site.register(Word)
# admin.site.register(WordInSentence)
#
# class TranslationInline(admin.StackedInline):  # You can also use admin.StackedInline if you prefer
#     model = Translation
#     fk_name = 'source_sentence'  # since the ForeignKey in the Translation model to Sentence is called source_sentence
#     extra = 1  # Number of empty forms displayed
#
# class SentenceAdmin(admin.ModelAdmin):
#     inlines = [TranslationInline, ]
#     list_display = ('sentence', 'language', 'complexity_rating', 'theme')
#     search_fields = ('sentence', )
#     list_filter = ('language', 'theme')
#
# admin.site.register(Sentence, SentenceAdmin)


from django import forms
from django.contrib import admin
from .models import Sentence, Language, Word, WordInSentence
from .services import store_sentence


class TranslationForm(forms.ModelForm):
    new_translation = forms.CharField(required=False, label='Add new translation',
                                      help_text='Add a new translation for this sentence')
    translation_language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False,
                                                  label='Translation language',
                                                  help_text='Specify the language for the new translation')
    class Meta:
        model = Sentence
        exclude = ['sentence_hash', 'complexity_rating']

    def save(self, commit=True):
        # Access the new_translation and translation_language fields from cleaned_data
        new_translation_text = self.cleaned_data.get('new_translation')
        translation_language = self.cleaned_data.get('translation_language')

        # Save the main instance (Sentence)
        instance = super().save(commit=commit)

        # If a new translation and its language are provided, save it
        if new_translation_text and translation_language:
            stored_sentence, message = store_sentence(new_translation_text, translation_language)
            instance.translated_sentences.add(stored_sentence)

        return instance


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    form = TranslationForm
    list_display = ('sentence', 'language', 'theme', 'type_display')
    fields = ('sentence', 'language', 'theme', 'type', 'new_translation', 'translation_language')
    readonly_fields = ('sentence',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        sentence = Sentence.objects.get(pk=object_id)
        # Add the existing translations to the context to be displayed
        translations = sentence.translated_sentences.all()
        extra_context['translations'] = translations
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def type_display(self, obj):
        """Display for the 'type' many-to-many field"""
        return ", ".join([str(type) for type in obj.type.all()])

    type_display.short_description = 'Type'



admin.site.register(Language)
admin.site.register(Word)
admin.site.register(WordInSentence)
