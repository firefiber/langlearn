from django.contrib import admin
from .models import Language, Word, Sentence, WordInSentence

admin.site.register(Language)
admin.site.register(Word)
admin.site.register(Sentence)
admin.site.register(WordInSentence)

