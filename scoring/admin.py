from django.contrib import admin
from .models import WordScore, Score, ComparisonMode

admin.site.register(WordScore)
admin.site.register(Score)


class ComparisonModeAdmin(admin.ModelAdmin):
    list_display = ['mode']

admin.site.register(ComparisonMode, ComparisonModeAdmin)
