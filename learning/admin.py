from django.contrib import admin
from .models import UserWordBank, UserSentence, UserWordDeck, UserWordBuffer

admin.site.register(UserSentence)
admin.site.register(UserWordBank)
admin.site.register(UserWordDeck)
admin.site.register(UserWordBuffer)



