from django.core.management.base import BaseCommand, CommandError

from languages.models import Language

import langcodes

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help='Language name')
        parser.add_argument('category', type=str, help='Category of the language: L - learning, N - native, B - Both')

    def handle(self, *args, **options):
        language_value = options['language']
        category = options['category']

        try:
            language_code = langcodes.find(language_value).language

            language_item = Language.objects.create(
                value=language_value,
                code=language_code,
                category=category

            )

        except LookupError:
            return f'Language code for "{language_value}" not found. Please verify language submitted is a valid language name, and try again.'

        self.stdout.write(self.style.SUCCESS(f'Successfully added language "{language_value}", with code "{language_code}", and category "{category}"'))