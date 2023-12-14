# LangLearn>learning>urls.py
from django.urls import path
from . import views
from .views import LearningView,CompareView,UserWordsAPIView

urlpatterns = [
    path('learning/', LearningView.as_view(), name='learning'),
    path('compare/', CompareView.as_view(), name='compare'),
    path('userwords/', UserWordsAPIView.as_view(), name='compare')
    # path('next_sentence/', views.next_sentence, name='next_sentence'),
    # path('compare/', views.compare, name='compare'),
]
