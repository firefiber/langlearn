import os
from django.core.management.base import BaseCommand
from languages.models import Word, Language
from learning.models import FrequencyWordDeck
import pandas as pd


class Command(BaseCommand):
    help = 'Import words from an Excel file'

    def handle(self, *args, **options):
        # Get the path to the Excel file relative to the current script
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'frequency_table.xlsx')

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        df = df[::-1]
        # Get the language instance for the desired language (e.g., Spanish)
        language = Language.objects.get(name='Spanish')

        # Iterate over the DataFrame rows and create Word instances
        for _, row in df.iterrows():
            word = Word.objects.create(
                language=language,
                word_item=row['lemma'],
            )

            FrequencyWordDeck.objects.create(
                language=language,
                word_item=word,
                frequency_rating=row['freq']
            )

        self.stdout.write(self.style.SUCCESS('Words imported successfully.'))
