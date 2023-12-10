from .base import *

############################################## COOKIES

CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

############################################## EMAIL

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)