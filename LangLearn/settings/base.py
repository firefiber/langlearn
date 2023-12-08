from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
import os

############################################## PROJECT DIRECTORIES

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BASE_DIR = os.path.join(ROOT_DIR, 'backend')

############################################## DJANGO SETTINGS

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)

############################################## NETWORKING

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

############################################## PROJECT SETTINGS

ROOT_URLCONF = 'LangLearn.urls'
WSGI_APPLICATION = 'LangLearn.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = '/'
# LOGIN_REDIRECT_URL = '/learning/'

# INTERNATIONALIZATION

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

############################################## INSTALLED APPS

INSTALLED_APPS = [
    # DEFAULT DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CUSTOM APPS
    'main.apps.MainConfig',
    'feedback.apps.FeedbackConfig',
    'languages.apps.LanguagesConfig',
    'learning.apps.LearningConfig',
    'reporting.apps.ReportingConfig',
    'scoring.apps.ScoringConfig',
    'user_management.apps.UserManagementConfig',

    # THIRD PARTY APPS
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'webpack_loader',
]

############################################## DJANGO CORE CONFIG

# MIDDLEWARE

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'templates']
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(ROOT_DIR, 'frontend/dist')]
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

# DATABASES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT', cast=int),
    }
}

# PASSWORD VALIDATION

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


############################################## STATIC FILES

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), os.path.join(ROOT_DIR, 'frontend/dist/')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

############################################## REST FRAMEWORK

# BASE DRF

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# DJOSER

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

# JWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
}

############################################## EMAIL

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

############################################## WEBPACK

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': os.path.join(BASE_DIR, 'path_to_vue_project/webpack-stats.json'),
    }
}


