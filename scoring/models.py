from django.db import models
from user_management.models import UserProfile

'''
This model records the score that each user has achieved for each word they've learned on each day. This is a 
many-to-many relationship between User and Word, as each user can have many word scores and each word can have many 
scores associated with different users. 
'''


class WordScore(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    word = models.ForeignKey('learning.UserWord', on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user_profile', 'word', 'date']), ]

    def __str__(self):
        return f'{self.user_profile.user.username}: {self.word.word} - {self.score}'


'''
This model records the overall score that each user has achieved on each day. Each user 
can have many scores (one for each day they've used the app). 
'''


class Score(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user_profile', 'date']), ]

    def __str__(self):
        return f'{self.user_profile.user.username}: {self.score}'



