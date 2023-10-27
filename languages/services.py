import hashlib

from django.core.exceptions import ObjectDoesNotExist
from .models import Language, Sentence
from django.db import transaction

def store_sentence(sentence_text, language_name):
    """
    Store a sentence in the database.

    Parameters:
    - sentence_text (str): The text of the sentence to be stored.
    - language_name (str): The name of the language of the sentence.

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

