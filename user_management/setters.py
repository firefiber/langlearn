from user_management.models import UserLanguageProficiency
from languages.models import Word


from django.core.cache import cache
from languages.models import Word, Language
from user_management.models import UserProfile


def update_frequency_range(user_profile, language):
    # Fetch the active proficiency instance for the user
    active_proficiency = user_profile.get_active_language_proficiency()

    # Ensure that the active proficiency is for the specified language
    if active_proficiency.language != language:
        raise Exception(f"The user's active learning language is not {language}")

    # Calculate the new frequency range
    total_word_count = Word.objects.filter(language=language).count()
    min_frequency = int(active_proficiency.buffer_location * total_word_count)
    max_frequency = int(min_frequency + active_proficiency.buffer_size * total_word_count)

    # Before updating the range, remove the old cache
    old_cache_key = f'{language.id}_{active_proficiency.buffer_range_start}_{active_proficiency.buffer_range_end}'
    cache.delete(old_cache_key)

    # Update the frequency range in the active proficiency
    active_proficiency.buffer_range_start = min_frequency
    active_proficiency.buffer_range_end = max_frequency
    active_proficiency.save()

    # Now that the range has been updated, fetch the new words and store them in the cache
    new_cache_key = f'{language.id}_{min_frequency}_{max_frequency}'
    words_in_buffer = list(Word.objects.filter(
        language=language,
        frequency_rating__range=(min_frequency, max_frequency)
    ))
    cache.set(new_cache_key, words_in_buffer, 60 * 60 * 24)  # Cache for 24 hours

    return min_frequency, max_frequency
