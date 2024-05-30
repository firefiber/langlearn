import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from learning.models import Deck, UserDeckSubscription, UserWordBuffer, UserDeckBufferWord

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Get the user profile and active deck
        user_profile = User.objects.get(username='test_user').userprofile
        deck = UserDeckSubscription.objects.get(user_profile=user_profile, is_active=True).deck

        # Get the buffer and entries
        buffer = UserWordBuffer.objects.get(deck=deck)
        buffer_items = UserDeckBufferWord.objects.filter(buffer=buffer)

        # Calculate weights based on priority and proficiency
        word_weights = []
        for item in buffer_items:
            # Setting a baseline proficiency of 1
            weight = item.priority / (1 + item.proficiency)
            word_weights.append((item.word_item.value, weight))

        # Normalize weights
        total_weight = sum(weight for _, weight in word_weights)
        words, weights = zip(*[(word, float(weight / total_weight)) for word, weight in word_weights])

        # Weighted random choice of 10 words from normalized weights
        sample_size = min(buffer_items.count(), 10)
        selected_words = random.choices(population=words, weights=weights, k=sample_size)

        # Output the selected words
        print(selected_words)



