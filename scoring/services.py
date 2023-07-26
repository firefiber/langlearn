import textdistance
from utils.languge_code_manager import LanguageCodeManager
from django.utils import timezone
from learning.models import Word, UserWord, Sentence, UserSentence, UserPracticeBuffer
from scoring.models import WordScore
from fuzzywuzzy import fuzz

class SentenceComparer:
    def __init__(self, language_code):
        self.language_manager = LanguageCodeManager(language_code)
        self.language_manager.initialize_tools()

        self.nlp = self.language_manager.nlp
        self.spell = self.language_manager.spell
        self.tool = self.language_manager.tool

    def compare_sentences(self, correct_sentence, user_sentence):
        # Tokenize sentences
        correct_tokens = correct_sentence.split()
        user_tokens = user_sentence.split()

        word_scores = []
        for i, correct_word in enumerate(correct_tokens):
            if i < len(user_tokens):
                user_word = user_tokens[i]
                score = fuzz.ratio(correct_word, user_word) / 100
            else:
                score = 0
            word_scores.append((correct_word, score))

        # Calculate overall similarity as the average of word scores
        similarity = sum(score for _, score in word_scores) / len(word_scores) if word_scores else 0

        return {
            "similarity": similarity,
            "word_scores": word_scores,
        }


class ScoreManager:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def calculate_and_update_scores(self, comparison_results, correct_sentence, user_sentence, language_code):
        # extract word_scores from comparison_results
        word_scores = comparison_results['word_scores']

        # update UserWord and WordScore models for each word and score
        for word, score in word_scores:
            # Check if a UserWord record already exists for this user and word
            user_word, created = UserWord.objects.get_or_create(
                user_profile=self.user_profile,
                word=word,
                defaults={'proficiency_level': score, 'last_practiced': timezone.now()}
            )

            # If the UserWord record already existed, update it
            if not created:
                # We could simply replace the proficiency level with the new score,
                # or we could do some kind of average or weighted average. Here we're just replacing it.
                user_word.proficiency_level = score
                user_word.last_practiced = timezone.now()
                user_word.save()

            # Create a new WordScore record with the score for this word
            WordScore.objects.create(
                user_profile=self.user_profile,
                word=user_word,
                score=score,
                date=timezone.now()
            )