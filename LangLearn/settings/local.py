from .base import *

############################################## DATABASES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'speasy_local',
        'USER': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

############################################## TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR.parent, 'frontend/dist')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

############################################## STATIC FILES

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

############################################## COOKIES

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE='False'

############################################## EMAIL

EMAIL_BACKEND = config('EMAIL_BACKEND')

