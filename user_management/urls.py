from django.urls import path
from .views import CustomLoginView, CustomLogoutView, CustomSessionView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('session/', CustomSessionView.as_view(), name='session')
]