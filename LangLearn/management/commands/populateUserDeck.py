import difflib

from django.core.management.base import BaseCommand

from user_management.models import User
from languages.models import Word, Language
from learning.models import Deck, UserDeck


class Command(BaseCommand):
    help = 'Populate a given user deck with words, submitted as a list of comma separated values.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('deck_name', type=str, help='Deck name')
        parser.add_argument('rank', type=float, help='Priority')
        parser.add_argument('word_list', type=str, help='Word list')


    def handle(self, *args, **options):
        username = options['username']
        deck_name = options['deck_name']
        input_word_list = options['word_list'].split(',')
        rank = options['rank']

        try:
            user = User.objects.get(username=username)
            deck = Deck.objects.get(name=deck_name)

            user_profile = user.userprofile
            active_language = user_profile.get_active_language_proficiency().language

            main_word_list = Word.objects.filter(language=active_language)

            for word in input_word_list:
                word_match = difflib.get_close_matches(word, [word_obj.value for word_obj in main_word_list], n=1)
                if word_match:
                    base_word = main_word_list.get(value=word_match[0])
                    deck_item = UserDeck.objects.create(
                        deck=deck,
                        user_profile=user_profile,
                        word_item=base_word,
                        rank=1.0
                    )

        except User.DoesNotExist:
            print('User does not exist. Please try again.')

        except Deck.DoesNotExist:
            print('Deck does not exist. Please try again.')