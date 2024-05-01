import hashlib
from statistics import mean
from django.db import models

'''
This model contains data related to the languages that the app supports. Each language has a name. 
This model is referenced by other models to link user_management, words, and sentences to a specific language. 
'''


class Language(models.Model):
    LANGUAGE_CATEGORIES = (
        ('L', 'Learning'),
        ('N', 'Native'),
        ('B', 'Both')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=1, choices=LANGUAGE_CATEGORIES, default='B')

    def __str__(self):
        return self.name


'''
This model contains the data about each word_item that user_management can learn. Each word_item is associated with a language and has 
a frequency_rating which indicates how common the word_item is. 
'''


class Word(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word_item = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=['word_item', ]), ]

    def __str__(self):
        return self.word_item


'''
This model stores sentence types.
'''


class SentenceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


'''
This model stores the sentences that users can practice translating. Each sentence is linked to a 
language and has a complexity_rating.
'''


class Sentence(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    sentence = models.TextField()
    sentence_hash = models.CharField(max_length=64, unique=True)
    translation = models.ManyToManyField("self", symmetrical=False, related_name='translated_sentences', blank=True)
    complexity_rating = models.FloatField(blank=True, null=True)
    theme = models.CharField(max_length=100, default="general", blank=True)
    type = models.ManyToManyField(SentenceType, blank=True)
    words = models.ManyToManyField(Word, blank=True)

    def get_translations(self):
        # Fetch translations using the many-to-many relationship
        return self.translated_sentences.all()

    def calculate_complexity(self):
        # Complexity based on length of the sentence
        length_complexity = self.calculate_length_complexity()

        # Complexity based on vocabulary
        vocabulary_complexity = self.calculate_vocabulary_complexity()

        # Final complexity score is a weighted average of the two complexities
        self.complexity_rating = 0.5 * length_complexity + 0.5 * vocabulary_complexity
        self.save()

    def calculate_length_complexity(self):
        # Adjust these thresholds as per your needs
        if len(self.sentence) <= 50:
            return 0.2
        elif len(self.sentence) <= 100:
            return 0.4
        elif len(self.sentence) <= 150:
            return 0.6
        elif len(self.sentence) <= 200:
            return 0.8
        else:
            return 1.0

    def calculate_vocabulary_complexity(self):
        word_complexities = []
        for word in self.words.all():
            word_complexities.append(word.frequency_rating)

        # Average complexity of words
        avg_word_complexity = mean(word_complexities)
        return avg_word_complexity

    def save(self, *args, **kwargs):
        # self.calculate_complexity()
        self.sentence_hash = hashlib.sha256(self.sentence.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sentence[:50]

'''
Intermediary model, used for storing translations into the database. 
'''
class Translation(models.Model):
    source_sentence = models.ForeignKey(Sentence, related_name="translations_from", on_delete=models.CASCADE)
    translated_sentence = models.ForeignKey(Sentence, related_name="translations_to", on_delete=models.CASCADE)
    source_language = models.ForeignKey(Language, related_name="translation_sources", on_delete=models.SET_NULL, null=True)
    translated_language = models.ForeignKey(Language, related_name="translated_languages", on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['source_sentence', 'translated_sentence']

    def __str__(self):
        return f"{self.source_sentence.sentence[:30]} -> {self.translated_sentence.sentence[:30]}"


'''
This model records which words appear in which sentences. This is a many-to-many relationship 
between Word and Sentence, as each sentence can contain many words and each word_item can appear in many sentences.
'''


class WordInSentence(models.Model):
    word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['word_item', 'sentence']), ]
