from django.db import transaction
from user_management.models import UserProfile
from .models import UserWordBank

class Utils(object):

    def __init__(self, user):
        self.user = user
        self.user_profile = UserProfile.objects.get(user=self.user)

    def update_or_create_user_word(self, word, **kwargs):
        user_word, created = UserWordBank.objects.get_or_create(
            user_profile = self.user_profile,
            word = word,
            defaults = {**kwargs}
        )

        if not created:
            for key, value in kwargs.items():
                setattr(user_word, key, value)
                user_word.save()

        return user_word