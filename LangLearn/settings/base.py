from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
import os

############################################## PROJECT DIRECTORIES

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# BASE_DIR = os.path.join(ROOT_DIR, 'backend')

############################################## DJANGO SETTINGS

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)

############################################## NETWORK ACCESS

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
    'LangLearn',

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
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS':{
        'user_create': 'user_management.serializers.UserRegistrationSerializer'
    }
}

# JWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
}


############################################## WEBPACK

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': os.path.join(BASE_DIR, 'path_to_vue_project/webpack-stats.json'),
    }
}
