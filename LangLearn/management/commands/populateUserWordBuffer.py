import sys

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from user_management.models import UserProfile, UserLearningLanguage
from learning.models import Deck, DeckWord, UserWordBuffer

import numpy as np

class UserNotActiveError(Exception):
    """Exception raised when a user account is not marked active."""
    pass

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="Username")

    def handle(self, *args, **options):
        username = options['username']

        try:
            # Get user and user profile
            user = User.objects.get(username=username)
            # If user account inactive, raise error
            if not user.is_active:
                raise UserNotActiveError

            user_profile = user.userprofile
            # Get active language data
            active_language_object = user_profile.get_active_language()
            active_language = active_language_object.language
            # Get active deck data
            deck = user_profile.get_active_deck(active_language)
            deck_words = DeckWord.objects.filter(deck=deck)[:10]
            # Create priority calculation function based on rank type
            if deck.rank_type == Deck.INTEGER:
                # If rank type is integer, interpolate from rank scale (1 - n) to priority scale (1.00 - 0.01)
                interp_input_range = [deck_words[0].rank, deck_words[len(deck_words) - 1].rank]
                interp_output_range = [1.00, 0.01]
                def calculate_priority(rank):
                    return np.round(np.interp(rank, interp_input_range, interp_output_range), 2)
            elif deck.rank_type == Deck.FLOAT:
                # If rank type is float (1.00 - 0.01), return rank as is.
                def calculate_priority(rank):
                    return rank
            # Loop over words in deck word items
            with transaction.atomic():
                for deck_word in deck_words:
                    # For each word, calculate priority, set the word item, and create buffer entry
                    priority = calculate_priority(deck_word.rank)
                    word_item = deck_word.word_item
                    user_word_buffer = UserWordBuffer.objects.create(
                        user_profile=user_profile,
                        language=active_language,
                        deck_source=deck,
                        word_item=word_item,
                        priority=priority
                    )

            self.stdout.write(self.style.SUCCESS(f'User word buffer successfully populated for "{username}", with words from deck "{deck.name}".'))

        except User.DoesNotExist:
            self.stderr.write(f'No user account found for "{username}". Please verify the user account exists.')

        except UserNotActiveError:
            self.stderr.write(f'User account for "{username}" not active. Please activate user account and try again.')

        except UserProfile.DoesNotExist:
            self.stderr.write(f'No user profile found for "{username}". Please verify the user has a user profile created.')

        except UserLearningLanguage.DoesNotExist:
            self.stderr.write(f'User "{username}" has no active language set.')

        except Deck.DoesNotExist:
            self.stderr.write(f'No active decks found. Please activate a deck for user "{username}" and try again.')





















    #     user = User.objects.get(username=options['user'])
    #     deck = apps.get_model('learning', options['deck'])
    #
    #     user_profile = user.userprofile
    #
    #     active_language = user_profile.get_active_language_proficiency().language
    #     active_language_id = active_language.id
    #
    #     deck_type = ContentType.objects.get_for_model(deck)
    #
    #     deck_items = deck.objects.filter(language=active_language_id)[:20]
    #     print(deck_items)
    #     input_range = [deck_items.first().frequency_rating, len(deck_items) - 1]
    #
    #     output_range = [0.9, 0.01]
    #
    #     for item in deck_items:
    #         print(item)
        #     priority = round(np.interp(item.frequency_rating, input_range, output_range), 2)
        #
        #     user_word_buffer = UserWordBuffer.objects.create(
        #         user_profile=user_profile,
        #         language=active_language,
        #         deck_type=deck_type,
        #         object_id=item.id,
        #         priority=priority
        #     )
        #
        #     try:
        #         user_word_buffer.clean()
        #     except ValidationError as e:
        #         print(f"Validation Error: {e}")
        #     else:
        #         user_word_buffer.save()
