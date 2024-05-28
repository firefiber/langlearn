import os
from itertools import islice

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from languages.models import Language, Word
from learning.models import Deck, DeckWord

import pandas as pd


class Command(BaseCommand):
    help = 'Create a system word deck, set to public visibility by default.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Deck name')
        parser.add_argument('language', type=str, help='Deck language')
        parser.add_argument('description', type=str, help='Deck description')
        parser.add_argument('ranked', type=str, help='Deck ranked - Y/N')
    def handle(self, *args, **options):
        deck_name = options['name']
        deck_lang = options['language']
        deck_desc = options['description']
        is_ranked = True if str(options['ranked']).lower() == 'y' else False

        project_root = settings.BASE_DIR
        source_columns = ('word', 'rank') if is_ranked else ('word', )

        # Access and read input source file and check if required columns exist
        try:
            file_path = os.path.join(project_root, 'languages', 'management', 'data', deck_name + '.xlsx')
            df = pd.read_excel(file_path)

            if not all(column in df.columns for column in source_columns):
                raise ValueError(f'Input source file does not contain required columns: {", ".join(source_columns)}')

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Deck input source file "{deck_name}" not found in language directory ("{file_path}")'))
            return

        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
            return

        # Check if language valid
        try:
            language = Language.objects.get(value=deck_lang)
        except Language.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Language "{deck_lang}" not found.'))
            return

        # Create deck
        try:
            deck = Deck.objects.create(
                name=deck_name,
                description=deck_desc,
                language=language,
                is_ranked=is_ranked,
            )

            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        word_item = Word.objects.get(value=row[source_columns[0]])
                        rank = row[source_columns[1]] if is_ranked else index + 1

                        deck_word_item = DeckWord.objects.create(
                            deck=deck,
                            word_item=word_item,
                            rank=rank
                        )

                    except Word.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Word "{word_item}" not found in the {language} word database.'))
                        return

                    except Exception as e:
                        return e

            self.stdout.write(self.style.SUCCESS(f'New word deck created and populated successfully.\n'
                                                 f'Name: {deck.name}\n'
                                                 f'Description: {deck.description}\n'
                                                 f'Language: {deck.language.value}\n'
                                                 f'is_ranked: {deck.is_ranked}\n'
                                                 f'Words: {deck.word_items.count()}'))

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'An error occurred while creating the deck: {str(e)}'))
            return

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))
            return
