#TODO: Rework UserWordBank to store words above a proficiency range
#TODO: Auto update proficiency?
#TODO: Test with selecting algo

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import UniqueConstraint
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q
from django.core.validators import MaxValueValidator, MinValueValidator
from user_management.models import UserProfile
from languages.models import Language, Word, Sentence
import numpy as np

##################### NEW MODELS TESTING #####################

# Base abstract model for all common deck information
# (name, language, visibility, etc).

class Deck(models.Model):
    VISIBILITY_OPTIONS = [
        (0, "Private"),
        (1, "Public")
    ]

    INTEGER = 'int'
    FLOAT = 'float'
    RANK_TYPES = [
        (INTEGER, 'Integer'),
        (FLOAT, 'Float')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word_items = models.ManyToManyField(Word, through='learning.DeckWord')
    rank_type = models.CharField(choices=RANK_TYPES, default=FLOAT)
    visibility = models.PositiveIntegerField(choices=VISIBILITY_OPTIONS, default=0)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.created_by and not self.visibility:
                self.visibility = 0
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'language'])
        ]
        unique_together = ['name', 'language', 'created_by']


class DeckWord(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
    rank = models.DecimalField(max_digits=7, decimal_places=2)

    def clean(self):
        super().clean()
        if self.deck.rank_type == self.deck.INTEGER:
            if self.rank % 1 != 0 or self.rank < 0:
                raise ValidationError(f'Rank must be a non-negative integer when rank type is set to {self.rank_type}')
        elif self.deck.rank_type == self.deck.FLOAT:
            if not (0 <= self.rank <= 1):
                raise ValidationError(f'Rank must be between 0.0 and 1.0 when rank type is set to {self.rank_type}')

    def __str__(self):
        return f'Deck: {self.deck.name}\nWord: {self.word_item.value}\nRank: {self.rank}'

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['deck', 'word_item'])
    #         ]

# Model to keep track of all decks users have
# subscribed to and active status
class UserDeckSubscription(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            UserDeckSubscription.objects.filter(
                user_profile=self.user_profile,
                is_active=True
            ).update(is_active=False)

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user_profile', 'deck')

##############################################################

# class Deck(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(max_length=1000)
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)
#     visibility = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'Name: {self.name}\nDescription: {self.description}'
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['name', 'language'])
#         ]

# class SystemDeck(models.Model):
#     deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='system_decks')
#     word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
#     rank = models.IntegerField()
#
#     class Meta:
#         ordering = ['rank']
#         constraints = [
#             UniqueConstraint(fields=['deck', 'word_item'], name='unique_systemdeck')
#         ]
#         indexes = [
#             models.Index(fields=['deck','word_item', 'rank'])
#         ]
#
# class UserDeck(models.Model):
#     deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='user_decks')
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
#     rank = models.DecimalField(
#         max_digits=2,
#         decimal_places=1,
#         validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
#     )
#     active = models.BooleanField(default=True)
#
#     class Meta:
#         ordering = ['rank']
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(rank__gte=0.0) & models.Q(rank__lte=1.0),
#                 name='UserDeck_rank_range'
#             ),
#             UniqueConstraint(fields=['deck', 'word_item'], name='unique_userdeck')
#         ]
#         indexes = [
#             models.Index(fields=['user_profile', 'rank', 'word_item'])
#         ]



# user buffer has fixed input slice size (from any given deck, only a max amount of words will be added at once to the buffer)
# buffer assigns input priority of each word:
# 	if ranked, by interpolating rank to priority scale (0.10 to 1.00)
# 	if unranked, by assigning a random priority between 0.10 and 1.00)
# buffer keeps track of deck size, and adds more once all current words are below 0.1 in priority
#
# buffer fields:
# 	- user_profile
# 	- language
# 	- deck
# 	- word_items
# 	-
#
# buffer functions:
# 	- custom save to track amount of entries
# 	- flush buffer
# 	- replenish from deck
# 		- if all items priority below 0.1, or empty (just initialized)
# 			- from deck source, get next section (from current + 1 to max size)

class UserWordBuffer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    deck_source = models.ForeignKey(Deck, on_delete=models.SET_NULL, null=True)
    word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
    priority = models.DecimalField(max_digits=3, decimal_places=2)
    proficiency = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    fail_pass_ratio = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    times_seen = models.IntegerField(default=0)
    times_passed = models.IntegerField(default=0)
    times_failed = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        # If number of entries
        print(UserWordBuffer.objects.count())
        super().save(*args, **kwargs)
    class Meta:
        indexes = [
            models.Index(fields=['user_profile', 'deck_source']),
            models.Index(fields=['user_profile', 'priority']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(proficiency__gte=0.00) & models.Q(proficiency__lte=1.00),
                name='UserWordBuffer_proficiency_range'
            )
        ]


'''
This model records which words a user is learning, their current proficiency level with each value, and the last 
time they practiced that value. This is a many-to-many relationship between User and Word, as each user can learn many 
words and each value can be learned by many user_management. 
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


# class UserSentence(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
#     proficiency_level = models.FloatField()
#     last_practiced = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         indexes = [models.Index(fields=['user_profile', 'sentence']), ]
#
#     def __str__(self):
#         return f'{self.user_profile.user.username}: {self.sentence.sentence}'


'''
This model stores the buffer of sentences that a user is currently practicing. It is a one-to-one relationship.
The buffer is stored as a JSONField for easy access and quick retrieval.
'''

# class FrequencyWordDeck(models.Model):
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)
#     word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
#     frequency_rating = models.IntegerField()
#
#     def __str__(self):
#         return f'{self.word_item}: {self.frequency_rating}'
#
#     class Meta:
#         ordering = ['frequency_rating']

# class UserWordDeck(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)
#     word_item = models.ForeignKey(Word, on_delete=models.CASCADE)
#     priority_rating = models.DecimalField(
#         max_digits=2,
#         decimal_places=1,
#         validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
#     )
#     date_created = models.DateTimeField(auto_now_add=True)
#     active = models.BooleanField(default=True)
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['user_profile']),
#         ]
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(priority_rating__gte=0.0) & models.Q(priority_rating__lte=1.0),
#                 name='UserWordDeck_priority_rating_range'
#             )
#         ]