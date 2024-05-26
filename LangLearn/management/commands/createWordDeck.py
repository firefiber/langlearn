import sys

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from languages.models import Language
from learning.models import Deck

class Command(BaseCommand):
    help = 'Create a system word deck, set to public visibility by default.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Deck name')
        parser.add_argument('language', type=str, help='Deck language')
        parser.add_argument('description', type=str, help='Deck description')

    def handle(self, *args, **options):
        deck_name = options['name']
        deck_lang = options['language']
        deck_desc = options['description']
        deck_rank_type = Deck.INTEGER

        try:
            deck_lang = Language.objects.get(value=options['language'])
            deck_visibility = 1

            deck = Deck.objects.create(
                name=deck_name,
                description=deck_desc,
                language=deck_lang,
                rank_type=deck_rank_type,
                visibility=deck_visibility
            )

            self.stdout.write(self.style.SUCCESS('System deck created successfully.'))

        except Language.DoesNotExist:
            return f'Language "{deck_lang}" does not exist."'
