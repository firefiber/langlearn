from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from learning.models import Deck
from languages.models import Language
from user_management.models import User

class Command(BaseCommand):
    help = 'Create a new user word deck, for a specified user.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('deck_name', type=str, help='Deck name')
        parser.add_argument('deck_desc', type=str, help='Deck description')

    def handle(self, *args, **options):
        username = options['username']
        deck_name = options['deck_name']
        deck_desc = options['deck_desc']
        deck_visibility = 0

        try:
            user = User.objects.get(username=username)
            active_language_object = user.userprofile.get_active_language_proficiency()

            if active_language_object is None:
                raise AttributeError("User has no active language selected. Please set an active language and try again.")

            active_language=active_language_object.language

            deck = Deck.objects.create(
                name=deck_name,
                description=deck_desc,
                language=active_language,
                visibility=deck_visibility
            )

        except User.DoesNotExist as e:
            print(f'Username not found: {username}. Please try again.')

        except AttributeError as e:
            print(e)

