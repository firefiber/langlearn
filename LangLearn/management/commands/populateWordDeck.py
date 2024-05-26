import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from languages.models import Language, Word
from learning.models import Deck, DeckWord

import pandas as pd

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('deck_name', type=str, help='Name of the desired deck.')
        parser.add_argument('deck_language', type=str, help='Language of the desired deck.')

    def handle(self, *args, **options):
        deck_name = options['deck_name']
        deck_lang = options['deck_language']

        try:
            language = Language.objects.get(value=deck_lang)
            deck = Deck.objects.get(name=deck_name, language=language)

            project_root = settings.BASE_DIR
            file_path = os.path.join(project_root, "languages/management/data", "frequency_table_cleaned.xlsx")

            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found.")

            existing_words = Word.objects.filter(language=language)
            df = pd.read_excel(file_path)

            with transaction.atomic():
                for _,row in df.iterrows():
                    word = row['lemma']
                    try:
                        word_item = Word.objects.get(value=word)

                        deck_item = DeckWord.objects.create(
                            deck = deck,
                            word_item = word_item,
                            rank = row['freq']
                        )
                    except Word.DoesNotExist as e:
                        return f'Word "{word}" not found.'

        except Language.DoesNotExist:
            return f'Language "{deck_lang}" not found. Please enter a valid language name.'

        except Deck.DoesNotExist:
            return f'Deck with name "{deck_name}" in language "{deck_lang}" not found. Please enter a valid deck name.'
