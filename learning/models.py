#TODO: Rework UserWordBank to store words above a proficiency range
#TODO: Auto update proficiency?
#TODO: Test with selecting algo

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import CheckConstraint, Q
from django.core.validators import MaxValueValidator, MinValueValidator
from user_management.models import UserProfile
from languages.models import Language, Word, Sentence
import numpy as np

class FrequencyWordDeck(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
    frequency_rating = models.IntegerField()

    def __str__(self):
        return f'{self.word_item.word_item}: {self.frequency_rating}'

    class Meta:
        ordering = ['frequency_rating']

class UserWordDeck(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
    priority_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_profile']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(priority_rating__gte=0.0) & models.Q(priority_rating__lte=1.0),
                name='UserWordDeck_priority_rating_range'
            )
        ]

class UserWordBuffer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    word_item = GenericForeignKey('content_type', 'object_id')
    priority = models.DecimalField(max_digits=3, decimal_places=2)
    proficiency = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    fail_pass_ratio = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    times_seen = models.IntegerField(default=0)
    times_passed = models.IntegerField(default=0)
    times_failed = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         if not self.language_id:
    #             active_language_proficiency = self.user_profile.get_active_language_proficiency()
    #             if active_language_proficiency:
    #                 self.language_id = active_language_proficiency.language_id
    #         try:
    #             deck = self.content_type.get_object_for_this_type(pk=self.object_id)
    #             if isinstance(deck, UserWordDeck):
    #                 self.priority = deck.priority_rating
    #             elif isinstance(deck, FrequencyWordDeck):
    #                     input_range = [FrequencyWordDeck.objects.first().frequency_rating, FrequencyWordDeck.objects.last().frequency_rating]
    #                     output_range = [0.90, 0.01]
    #                     self.priority = np.interp(deck.frequency_rating, input_range, output_range)
    #             else:
    #                 raise ValueError(f"Unknown deck type: {type(deck)}")
    #         except ObjectDoesNotExist:
    #                 raise ValueError("Deck does not exist")
    #         super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['user_profile', 'content_type', 'object_id']),
            models.Index(fields=['user_profile', 'priority']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(priority__gte=0.00) & models.Q(priority__lte=0.5),
                name='UserWordBuffer_priority_range'
            ),
            models.CheckConstraint(
                check=models.Q(proficiency__gte=0.00) & models.Q(proficiency__lte=1.00),
                name='UserWordBuffer_proficiency_range'
            )
        ]


'''
This model records which words a user is learning, their current proficiency level with each word_item, and the last 
time they practiced that word_item. This is a many-to-many relationship between User and Word, as each user can learn many 
words and each word_item can be learned by many user_management. 
'''

class UserWordBank(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
    proficiency_level = models.FloatField()
    last_practiced = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user_profile', 'word_item']), ]

    def __str__(self):
        return f'{self.user_profile.user.username}: {self.word_item}'


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

