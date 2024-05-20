import os, sys

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from languages.models import Word, Language

import pandas as pd


class Command(BaseCommand):
    help = 'Import words from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help="Language")

    def handle(self, *args, **options):
        try:
            # Get the path to the Excel file relative to the current script
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'frequency_table_cleaned.xlsx')

            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found.")
            # Get the language item
            language = Language.objects.get(value=options['language'])

            # Read in the file
            df = pd.read_excel(file_path)

            # Loop over rows in file
            for _, row in df.iterrows():
                # Create a Word item for each item
                word = Word.objects.create(
                    language=language,
                    value=row['lemma']
                )

            self.stdout.write(self.style.SUCCESS('Words populated successfully.'))

        except FileNotFoundError:
            print("File not found.")
            sys.exit()

        except ObjectDoesNotExist:
            print("Language does not exist.")
            sys.exit()

