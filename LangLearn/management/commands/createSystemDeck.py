import sys

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps

from languages.models import Language
from learning.models import DeckVisibility, Deck

class Command(BaseCommand):
    help = 'Create a system word deck, set to public visibility by default.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Deck name')
        parser.add_argument('language', type=str, help='Deck language')
        parser.add_argument('description', type=str, help='Deck description')


    def handle(self, *args, **options):
        try:
            deck_name = options['name']
            deck_lang = Language.objects.get(value=options['language'])
            deck_desc = options['description']
            deck_visibility = DeckVisibility.objects.get(value='public')

            deck = Deck.objects.create(
                name=deck_name,
                description=deck_desc,
                language=deck_lang,
                visibility=deck_visibility
            )

            self.stdout.write(self.style.SUCCESS('System deck created successfully.'))

        except ObjectDoesNotExist as e:
            print(e)
            sys.exit()