from .base import *

DEBUG = False
CSRF_TRUSTED_ORIGINS = ['https://langlearn-development.up.railway.app']


SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Set to False if not using HTTPS
CSRF_COOKIE_SECURE = True  # Set to False if not using HTTPS
CSRF_COOKIE_HTTPONLY = True