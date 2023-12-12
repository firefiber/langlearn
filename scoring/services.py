import textdistance
from utils.languge_code_manager import LanguageCodeManager
from django.utils import timezone
from learning.models import Word, UserWord, Sentence, UserSentence, UserPracticeBuffer
from scoring.models import WordScore
from fuzzywuzzy import process
from unidecode import unidecode

######
from .models import ComparisonMode
######




class SentenceComparer:
    def __init__(self, language_code):
        self.language_manager = LanguageCodeManager(language_code)
        self.language_manager.initialize_tools()

        self.nlp = self.language_manager.nlp
        self.spell = self.language_manager.spell
        # self.tool = self.language_manager.tool

        self.mode = ComparisonMode.objects.first().mode

    def normalize_sentence(self,s):
        return unidecode(s)

    def get_best_match(self, word, correct_tokens):
        best_match, score = process.extractOne(word, correct_tokens)
        if score > 90:
            return best_match
        return word


    def compare_sentences(self, correct_sentence, user_sentence):
        correct_tokens = set(self.normalize_sentence(correct_sentence).split())
        user_tokens = set(self.normalize_sentence(user_sentence).split())

        user_tokens_corrected = set([self.get_best_match(word, correct_tokens) for word in user_tokens])
        common_tokens = correct_tokens.intersection(user_tokens_corrected)

        word_scores = []
        for word in common_tokens:
            word_scores.append((word,1))

        if self.mode == 'B':
            similarity = len(common_tokens)/len(correct_tokens) if user_tokens else 0
        else:
            similarity = 1 if correct_tokens == user_tokens_corrected else 0

        return {
            "similarity": similarity,
            "word_scores": word_scores
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

            # If the UserWord record already exists, update it
            if not created:
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




    # def compare_sentences(self, correct_sentence, user_sentence):
    #     # Tokenize sentences
    #
    #     correct_tokens = set(self.normalize_sentence(correct_sentence).split())
    #     user_tokens = set(self.normalize_sentence(user_sentence).split())
    #
    #     user_tokens_corrected = set([self.get_best_match(word, correct_tokens) for word in user_tokens])
    #
    #     common_tokens = correct_tokens.intersection(user_tokens_corrected)
    #
    #     print(common_tokens)
    #     word_scores = []
    #
    #     for word in common_tokens:
    #         word_scores.append((word, 1))
    #
    #     # Calculate similarity ratio (number of common words divided by total number of user words)
    #     if len(user_tokens) == 0:
    #         similarity = 0
    #     else:
    #         similarity = len(common_tokens) / len(correct_tokens)
    #
    #     return {
    #         "similarity": similarity,
    #         "word_scores": word_scores
    #     }