from django.core.management.base import BaseCommand
from languages.models import Word
from learning.models import FrequencyWordDeck

class Command(BaseCommand):
    help = 'Populate FrequencyWordDeck with existing words'

    def handle(self, *args, **kwargs):
        existing_words = Word.objects.all()

        for word in existing_words:
            FrequencyWordDeck.objects.create(
                word_item=word,
                frequency_rating=word.frequency_rating
            )

        self.stdout.write(self.style.SUCCESS('FrequencyWordDeck populated successfully.'))
