from .base import *

############################################## COOKIES

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

############################################## EMAIL

EMAIL_BACKEND = config('EMAIL_BACKEND')

