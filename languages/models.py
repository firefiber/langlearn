from statistics import mean
from django.db import models

'''
This model contains data related to the languages that the app supports. Each language has a name. 
This model is referenced by other models to link user_management, words, and sentences to a specific language. 
'''


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


'''
This model contains the data about each word that user_management can learn. Each word is associated with a language and has 
a frequency_rating which indicates how common the word is. 
'''


class Word(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    frequency_rating = models.IntegerField()
    pos = models.CharField(max_length=2)

    class Meta:
        indexes = [models.Index(fields=['word', ]), ]

    def __str__(self):
        return self.word


'''
This model stores sentence types.
'''


class SentenceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


'''
This model stores the sentences that user_management can practice translating. Each sentence is linked to a 
language and has a complexity_rating.
'''


class Sentence(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    sentence = models.TextField()
    translation = models.TextField(null=True, blank=True)
    complexity_rating = models.FloatField()
    theme = models.CharField(max_length=100, default="general")
    type = models.ManyToManyField(SentenceType)
    words = models.ManyToManyField(Word)

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
        self.calculate_complexity()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sentence[:50]


'''
This model records which words appear in which sentences. This is a many-to-many relationship 
between Word and Sentence, as each sentence can contain many words and each word can appear in many sentences.
'''


class WordInSentence(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['word', 'sentence']), ]
