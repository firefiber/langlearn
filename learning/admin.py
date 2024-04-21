from django.contrib import admin
from .models import UserWordBank, UserSentence, UserWordDeck, UserWordBuffer, FrequencyWordDeck

admin.site.register(UserSentence)
admin.site.register(UserWordBank)
admin.site.register(UserWordDeck)
admin.site.register(UserWordBuffer)
admin.site.register(FrequencyWordDeck)


