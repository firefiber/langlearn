from django.db import models
from django.db.models import CheckConstraint, Q
from django.core.validators import MaxValueValidator, MinValueValidator
from user_management.models import UserProfile
from languages.models import Language, Word, Sentence

'''
This model records which words a user is learning, their current proficiency level with each word, and the last 
time they practiced that word. This is a many-to-many relationship between User and Word, as each user can learn many 
words and each word can be learned by many user_management. 
'''


class UserWordBank(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    wordItem = models.CharField(max_length=100)
    proficiency_level = models.FloatField()
    last_practiced = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user_profile', 'wordItem']), ]

    def __str__(self):
        return f'{self.user_profile.user.username}: {self.wordItem}'


class UserWordDeposit(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_word = models.CharField(max_length=100)
    date_of_entry = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )

    class Meta:
        indexes = [models.Index(fields=['user_profile', 'user_word', 'weight', 'date_of_entry']), ]
        constraints = [
            CheckConstraint(
                check=Q(weight__gte=0.0) & Q(weight__lte=1.0),
                name='UserWordDeposit_weight_range'
            )
        ]

'''
This model records which sentences a user is learning, their current proficiency level with each sentence, 
and the last time they practiced that sentence. This is a many-to-many relationship between User and Sentence, 
as each user can learn many sentences and each sentence can be learned by many user_management. 
'''


class UserSentence(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    proficiency_level = models.FloatField()
    last_practiced = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user_profile', 'sentence']), ]

    def __str__(self):
        return f'{self.user_profile.user.username}: {self.sentence.sentence}'


'''
This model stores the buffer of sentences that a user is currently practicing. It is a one-to-one relationship.
The buffer is stored as a JSONField for easy access and quick retrieval.
'''


class UserPracticeBuffer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    buffer = models.JSONField(default=dict)

    class Meta:
        indexes = [models.Index(fields=['user_profile']), ]
        unique_together = ('user_profile', 'language')

    def __str__(self):
        return f'{self.user_profile.user.username} Buffer ({self.language.name})'

    def save(self, *args, **kwargs):
        if not self.language_id:
            active_language_proficiency = self.user_profile.get_active_language_proficiency()
            if active_language_proficiency:
                self.language_id = active_language_proficiency.language_id
        super().save(*args, **kwargs)

    def save_buffer(self, buffer):
        self.buffer = buffer
        self.save()
