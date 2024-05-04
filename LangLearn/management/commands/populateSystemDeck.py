import os, sys

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.apps import apps

from languages.models import Language, Word
from learning.models import DeckVisibility, Deck, SystemDeck

import pandas as pd

class Command(BaseCommand):
    help = 'Populate a given system word deck, from a given input source.'

    def add_arguments(self, parser):
        parser.add_argument('deck_name', type=str, help='Deck name')

    def handle(self, *args, **options):
        try:
            deck = Deck.objects.get(name=options['deck_name'])
            language = deck.language

            project_root = settings.BASE_DIR
            file_path = os.path.join(project_root, "languages/management/data", "frequency_table_cleaned.xlsx")

            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found.")

            existing_words = Word.objects.filter(language=language)
            df = pd.read_excel(file_path)

            for _,row in df.iterrows():
                word = Word.objects.get(value=row['lemma'])

                deck_item = SystemDeck.objects.create(
                    deck = deck,
                    word_item = word,
                    rank = row['freq']
                )

        except ObjectDoesNotExist as e:
            print(e)
            sys.exit()

        except FileNotFoundError as e:
            print(e)
            sys.exit()