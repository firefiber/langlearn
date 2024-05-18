import sys

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from learning.models import Deck, SystemDeck, UserDeck, UserWordBuffer

import numpy as np

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="Username")
        parser.add_argument('deck_type', type=str, help="Input source deck type (system_decks or user_decks)")
        parser.add_argument('deck_name', type=str, help="Input source deck name")

    def handle(self, *args, **options):
        username = options['username']
        deck_type = options['deck_type']
        deck_name = options['deck_name']

        try:
            # Get the user
            user = User.objects.get(username=username)
            # Get the deck wrapper
            deck = Deck.objects.get(name=deck_name)
            # Get the deck items
            deck_items = getattr(deck, deck_type).all()[:100]
            # Get the userprofile
            user_profile = user.userprofile
            # Get the active learning language object
            active_language_object = user_profile.get_active_language_proficiency()
            # Exception if no active language found
            if active_language_object is None:
                raise AttributeError("User has not active language selected. Please set an active language and try again.")
            # Get the active learning language
            active_language = active_language_object.language
            # Get content type
            content_type = ContentType.objects.get_for_model(deck)
            # Define input and output ranges for rank to priority mapping
            input_range = [deck_items.first().rank, deck_items[len(deck_items) - 1].rank]
            output_range = [0.9, 0.1]

            for item in deck_items:
                value = item.rank
                priority_mapped = np.interp(value, input_range, output_range)
                priority_rounded = round(priority_mapped, 2)

                user_buffer_item = UserWordBuffer.objects.create(
                    user_profile=user_profile,
                    language=active_language,
                    deck_source=content_type,
                    object_id=item.id,
                    word_item=item.word_item,
                    priority=priority_rounded
                )

        except User.DoesNotExist:
            print(f"Username not found: {username}. Please try again.")

        except Deck.DoesNotExist:
            print("Deck not found. Please try again.")

        except ObjectDoesNotExist as e:
            print("Model not found.")
            sys.exit()

        except LookupError:
            print("Deck not found.")
            sys.exit()

































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
