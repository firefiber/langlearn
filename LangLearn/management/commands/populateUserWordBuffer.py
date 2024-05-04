import sys

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from languages.models import Language
from learning.models import FrequencyWordDeck, UserWordBuffer

import numpy as np


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user', type=str, help="Username")
        parser.add_argument('deck', type=str, help="Deck type")

    def handle(self, *args, **options):
        try:
        # Get the deck model
            deck = apps.get_model('learning', options['deck'].lower())
            # Get the user
            user = User.objects.get(username=options['user'])
            # Get the userprofile
            user_profile = user.userprofile
            # Get the active learning language
            active_language = user_profile.get_active_language_proficiency().language
            # Get the active learning language id
            acitve_language_id = active_language.id
            # Get deck type from deck model
            deck_type = ContentType.objects.get_for_model(deck)

            # if deck_type == ""
                # Get deck_items filtered by active language and buffer start and end frequency range (100)
                    # For each deck item
                        # Set priority to interpolation of item's frequency_rating from frequency range (1 to 100) to priority range (0.9 to 0.1)
                        # Create new UserWordBuffer item
                        # Set user_profile, language, deck_type
                        # Set object id to current items id
                        # Set priority
                        # Validate and save entry
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
