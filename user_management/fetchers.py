from django.core.cache import cache
from user_management.models import UserProfile
from learning.models import UserPracticeBuffer
from languages.models import Word


def fetch_user_info(username):
    user_profile = UserProfile.objects.get(user__username=username)
    active_proficiency = user_profile.get_active_language_proficiency()

    if not active_proficiency:
        raise Exception("No active learning language found for this user.")

    user_word_list = fetch_words_in_buffer(user_profile)

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
