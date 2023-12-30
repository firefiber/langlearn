from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserDataView, UserTrainingDataView, CustomSessionView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('session/', CustomSessionView.as_view(), name='session'),
    path('data/', UserDataView.as_view(), name='data'),
    path('training/', UserTrainingDataView.as_view(), name='training')
]