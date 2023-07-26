# LangLearn>learning>urls.py
from django.urls import path
from . import views  # import the views from the same directory

urlpatterns = [
    path('', views.home, name='home'),
    path('next_sentence/', views.next_sentence, name='next_sentence'),
    path('compare/', views.compare, name='compare'),
]
