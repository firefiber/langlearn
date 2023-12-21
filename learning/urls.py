# LangLearn>learning>urls.py
from django.urls import path
from . import views
from .views import LearningView,CompareView,UserWordsView,SessionView

urlpatterns = [
    path('learning/', LearningView.as_view(), name='learning'),
    path('compare/', CompareView.as_view(), name='compare'),
    path('userwords/', UserWordsView.as_view(), name='compare'),
    path('session/', SessionView.as_view(), name='session')
    # path('next_sentence/', views.next_sentence, name='next_sentence'),
    # path('compare/', views.compare, name='compare'),
]
