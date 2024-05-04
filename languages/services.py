import hashlib

from django.core.exceptions import ObjectDoesNotExist
from .models import Language, Sentence
from django.db import transaction

def store_sentence_translation_pair(pair):
    #Stores sentence pairs, then links them together
    original_sentence, original_message = store_sentence(pair["sentence"], pair["sentence_language"])
    if original_sentence is None:
        return None, original_message

    translation_sentence, translation_message = store_sentence(pair["translation"], pair["translation_language"])
    if translation_sentence is None:
        return None, translation_message

    with transaction.atomic():
        original_sentence.translation.add(translation_sentence)
        translation_sentence.translation.add(original_sentence)

    return (original_sentence, translation_sentence), "Sentences stored and linked successfully."

def store_sentence(sentence_text, language_name):
    """
    Store a sentence in the database.

    Parameters:
    - sentence_text (str): The text of the sentence to be stored.
    - language_name (str): The value of the language of the sentence.

    Returns:
    - sentence (Sentence): The stored sentence instance.
    - message (str): A message indicating the success or failure of the operation.
    """

    try:
        # Get the language object
        language = Language.objects.get(name=language_name)
        # Create hash
        sentence_hash = hashlib.sha256(sentence_text.encode()).hexdigest()

        # Check if the sentence already exists.
        try:
            sentence = Sentence.objects.get(sentence_hash=sentence_hash)
            return sentence, "Sentence already exists."

        except Sentence.DoesNotExist:
            pass

        # If it does not exist, create a sentence item and store it
        with transaction.atomic():
            sentence = Sentence.objects.create(
                sentence=sentence_text,
                language=language
            )

        return sentence, "Sentence stored successfully."

    except ObjectDoesNotExist:
        return None, f"Language {language_name} does not exist."

    except Exception as e:
        return None, f"An error occured: {str(e)}"


'''
get dict with sentence/trasnlation pairs
for each pair
    store sentence
    store translation
    link sentence and translation

'''