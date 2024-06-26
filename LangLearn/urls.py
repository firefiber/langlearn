from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('learning.urls')),
    path('auth/', include('djoser.urls')),
    path('user/', include('user_management.urls')),
    # path('', TemplateView.as_view(template_name='index.html')),
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

