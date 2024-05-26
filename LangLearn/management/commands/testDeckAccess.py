from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from learning.models import Deck, UserWordBuffer

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user', type=str, help='Username')
        parser.add_argument('deck_name', type=str, help='Deck name')

    def handle(self, *args, **options):
        username = options['user']
        deck_name = options['deck_name']

        user = User.objects.get(username=username)
        # user_decks = Deck.objects.filter(user_decks__user_profile=user.userprofile).distinct()
        deck = Deck.objects.get(name=deck_name)
        deck_items = UserDeck.objects.filter(user_profile=user.userprofile)
        # deck = user_decks.filter(name=deck_name)
        print(deck)

