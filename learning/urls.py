# LangLearn>learning>urls.py
from django.urls import path
from . import views
from .api import SimpleDataAPI

urlpatterns = [
    path('', views.learning, name='learning'),
    path('next_sentence/', views.next_sentence, name='next_sentence'),
    path('compare/', views.compare, name='compare'),
    path('api/simple-data/', SimpleDataAPI.as_view(), name='simple-data-api')
]
