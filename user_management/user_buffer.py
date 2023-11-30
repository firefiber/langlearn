#TODO: Rework entire flow - lots of redundancy here.

from django.core.cache import cache
from user_management.models import UserProfile, UserLanguageProficiency
from learning.models import UserWord
from languages.models import Word
import numpy as np
from django.utils import timezone
import datetime

NEW_WORD_WEIGHT = 1.0  # configurable


def fetch_user_info(username):
    user_profile = UserProfile.objects.get(user__username=username)
    active_proficiency = user_profile.get_active_language_proficiency()

    if not active_proficiency:
        raise Exception("No active learning language found for this user.")

    user_word_list = fetch_words_in_buffer(user_profile)
    user_learned_words = fetch_user_words(user_profile)
    learned_word_count = len(user_learned_words)

    # Including user_profile and active_proficiency in the result
    info = {
        'user_profile': user_profile,
        'learning_language': active_proficiency.language,
        'native_language': user_profile.native_language,
        'proficiency': active_proficiency.proficiency_level,
        'proficiency_weights': active_proficiency.proficiency_weights,
        'buffer_range_start': active_proficiency.buffer_range_start,
        'buffer_range_end': active_proficiency.buffer_range_end,
        'words': user_word_list,
        'learned_word_count': learned_word_count

        # Include other fields from active_proficiency as needed
    }

    return info

def fetch_words_in_buffer(user_profile):
    # Get the active proficiency
    active_proficiency = user_profile.get_active_language_proficiency()

    # Create a unique cache key based on the language and buffer range
    cache_key = f'{active_proficiency.language.id}_{active_proficiency.buffer_range_start}_{active_proficiency.buffer_range_end}'
    words_in_buffer = cache.get(cache_key)

    # If the words aren't in the cache, fetch them from the database and store them in the cache
    if words_in_buffer is None:
        words_in_buffer = list(Word.objects.filter(
            language=active_proficiency.language,
            frequency_rating__range=(active_proficiency.buffer_range_start, active_proficiency.buffer_range_end)
        ))
        cache.set(cache_key, words_in_buffer, 60 * 60 * 24)  # Cache for 24 hours

    return words_in_buffer


def fetch_user_words(user_profile):
    """
    Fetch user-specific word data for a given user and language.
    """
    # Fetch main buffer word list
    main_buffer = fetch_words_in_buffer(user_profile)

    # Extract word list from main buffer
    main_buffer_word_list = [word.word for word in main_buffer]

    # Fetch UserWords for the user and language
    user_words_queryset = UserWord.objects.filter(user_profile=user_profile)

    # Filter the UserWords based on the main_buffer_word_list
    user_words = user_words_queryset.filter(word__in=main_buffer_word_list)

    return user_words


def calculate_practice_buffer(main_buffer, user_words, buffer_size):
    """
    Calculate practice buffer based on the user's main buffer, user words and other criteria.
    """
    # Create a list of user words for easy look-up
    user_word_dict = {user_word.word: user_word for user_word in user_words}

    # Calculate weights for all words in the buffer
    weights = []
    for word in main_buffer:
        user_word = user_word_dict.get(word.word)
        # print(user_word.last_practiced, ", ", user_word.proficiency_level)

        if user_word:
            # Calculate weight based on proficiency and last practiced time
            days_since_last_practiced = (timezone.now() - user_word.last_practiced).days
            weight = (1 - user_word.proficiency_level) + days_since_last_practiced / 7 + 0.01
        else:
            # Assign default weight for new words
            weight = NEW_WORD_WEIGHT
        weights.append(weight)

    # Normalize weights
    total_weight = sum(weights)
    weights = [weight / total_weight for weight in weights]

    # Use weighted random selection to choose words for the practice buffer
    practice_buffer = np.random.choice(main_buffer, size=buffer_size, replace=False, p=weights)
    practice_buffer = [word.word for word in practice_buffer]
    # print(practice_buffer)
    return list(practice_buffer)


def get_practice_buffer(username):
    """
    Main function that fetches the user's information, main buffer, user words, and calculates the practice buffer.
    """
    user_info = fetch_user_info(username)
    user_profile = user_info['user_profile']
    language = user_info['learning_language']

    main_buffer = fetch_words_in_buffer(user_profile)
    # print("main_buffer", main_buffer)
    user_words = fetch_user_words(user_profile)
    # print("user_words", user_words)

    practice_buffer = calculate_practice_buffer(main_buffer, user_words, 5)

    return practice_buffer
