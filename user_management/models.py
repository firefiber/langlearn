from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from django.core.exceptions import ObjectDoesNotExist

from languages.models import Language

'''

'''

# TODO: change native_language related name to 'native_users'
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    learning_languages = models.ManyToManyField(Language, through='user_management.UserLearningLanguage', related_name='learning_users')
    native_language = models.ForeignKey(Language, related_name='native_language', on_delete=models.SET_NULL, null=True, blank=True)
    subscribed_decks = models.ManyToManyField('learning.Deck', through='learning.UserDeckSubscription', blank=True)

    def __str__(self):
        return self.user.username

    def get_active_language(self):
        active_learning_language = UserLearningLanguage.objects.filter(user_profile=self,
                                                                       is_active=True).first()
        if active_learning_language is None:
            raise ObjectDoesNotExist('No active language set for this user.')
        return active_learning_language

    def get_active_deck(self, language):
        from learning.models import UserDeckSubscription

        active_deck_subscription = UserDeckSubscription.objects.filter(user_profile=self,
                                                           deck__language=language,
                                                           is_active=True).first()

        if active_deck_subscription is None:
            raise ObjectDoesNotExist('No active subscribed decks found for this user.')
        return active_deck_subscription.deck

    class Meta:
        indexes = [
            models.Index(fields=['user',])
        ]


'''

'''

def default_weights():
    return {
        "comprehension": 0.00,
        "composition": 0.00,
        "communication": 0.00,
        "translation": 0.00
    }


class UserLearningLanguage(models.Model):
    BUFFER_LENGTH = 100

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    proficiency_level = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    proficiency_weights = JSONField(default=default_weights)

    is_active = models.BooleanField(default=False)

    buffer_size = models.FloatField(default=0.1)
    buffer_location = models.FloatField(default=0.0)

    buffer_range_start = models.IntegerField(default=0)
    buffer_range_end = models.IntegerField(default=500)

    class Meta:
        indexes = [
            models.Index(fields=['user_profile', 'language', 'is_active'])
        ]
        unique_together = ('user_profile', 'language')

    def save(self, *args, **kwargs):
        # If this proficiency is being set to active, deactivate the currently active one first
        if self.is_active:
            UserLearningLanguage.objects.filter(
                user_profile=self.user_profile,
                is_active=True
            ).update(is_active=False)

        super().save(*args, **kwargs)  # Call the original save method


