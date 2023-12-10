from .base import *

############################################## COOKIES

CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

############################################## EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
