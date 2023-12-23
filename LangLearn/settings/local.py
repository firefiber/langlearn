from .base import *

############################################## COOKIES

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'None'

############################################## EMAIL

EMAIL_BACKEND = config('EMAIL_BACKEND')

