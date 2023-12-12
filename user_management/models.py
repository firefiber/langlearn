#TODO: Move language proficiency model to learning models - better separation (HUGE WORK!! - lots of places referenced)

from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from languages.models import Language


'''
This model represents a user profile associated with a User account. It extends the User model
with additional fields and establishes a one-to-one relationship with the User model.
Each user profile has learning languages, a native language, a buffer size, and a buffer location.
'''


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    learning_languages = models.ManyToManyField(Language, through='UserLanguageProficiency', related_name='learning_users')
    native_language = models.ForeignKey(Language, related_name='native_language', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_active_language_proficiency(self):
        return self.userlanguageproficiency_set.filter(is_active=True).first()


'''
This model represents the language proficiencies of user_management. It establishes a many-to-many relationship 
between UserProfile and Language through UserLanguageProficiency.
Each UserLanguageProficiency instance links a user profile, a language, and a proficiency level.
'''


def default_weights():
    return {
        "vocabulary_complexity": 0.0,
        "syntactic_complexity": 0.0,
        "lexical_density": 0.0,
        # add other complexity metrics here...
    }


class UserLanguageProficiency(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    proficiency_level = models.FloatField(default=0.0)
    proficiency_weights = JSONField(default=default_weights)

    is_active = models.BooleanField(default=False)

    buffer_size = models.FloatField(default=0.1)
    buffer_location = models.FloatField(default=0.0)

    buffer_range_start = models.IntegerField(default=0)
    buffer_range_end = models.IntegerField(default=500)

    class Meta:
        unique_together = ('user_profile', 'language')

    def save(self, *args, **kwargs):
        # If this proficiency is being set to active, deactivate the currently active one first
        if self.is_active:
            UserLanguageProficiency.objects.filter(
                user_profile=self.user_profile,
                is_active=True
            ).update(is_active=False)

        super().save(*args, **kwargs)  # Call the original save method


