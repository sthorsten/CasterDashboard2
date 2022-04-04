"""
    Base settings for the Django Backend
"""

import os
from datetime import timedelta
from tkinter import ALL
from django.core.exceptions import ImproperlyConfigured
import environ

# region Base config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WSGI_APPLICATION = 'caster_dashboard_2.routing.application'
ASGI_APPLICATION = 'caster_dashboard_2.routing.application'

# endregion

# region Django config

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'channels',
    'corsheaders',
    'core.apps.CoreConfig',
    'main.apps.MainConfig',
    'match.apps.MatchConfig',
    'user.apps.UserConfig',
    'overlays.apps.OverlaysConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'caster_dashboard_2.urls'
LOGIN_URL = '/admin/login'

# Password Hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}

# endregion

# region REST Framwork / Authentication

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer', 'Token',)
}

# Prevent client-side javscript from accessing the token
# to prevent axios from sending the cookie in POST requests
CSRF_COOKIE_HTTPONLY = True

# endregion

# region USER / HOST CONFIG SECTION

# Read from environment file
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, "..", ".env"))

DEBUG = env('DEBUG', cast=bool)
MODE = env('MODE')
SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env('REDIS_HOST'), env('REDIS_PORT', cast=int))],
        },
    },
}

STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')

# if MODE == 'production':
#     STATIC_ROOT = os.path.join(BASE_DIR, "assets")
#     STATICFILES_DIRS.append(os.path.join(BASE_DIR, "static"))
# else:
#     STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Registration config
REGISTRATION_ENABLED = env('REGISTRATION_ENABLED', cast=bool)

# Allowed Hosts / Origins
# Includes localhost and the internal docker network ("dashboard") by default

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'backend',  # Docker
    'frontend'  # Docker
]

ALLOWED_HOSTS = ALLOWED_HOSTS + env('ALLOWED_HOSTS', cast=[str])
CSRF_TRUSTED_ORIGINS = []

for host in ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS.append(f"http://{host}")
    CSRF_TRUSTED_ORIGINS.append(f"https://{host}")

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

if MODE == 'development':
    CORS_ALLOW_ALL_ORIGINS = True

# endregion

# region Logging Configuration

LOGGING = {}

try:
    LOGGING = env('LOGGING')

except ImproperlyConfigured:
    # Use default configuration
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[{asctime}] [{name}] [{levelname}] {message}',
                'style': '{'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'django': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f"{BASE_DIR}/../logs/django.log",
                'formatter': 'default',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 5
            },
            'caster_dashboard': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f"{BASE_DIR}/../logs/caster_dashboard.log",
                'formatter': 'default',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 5
            },
            'errors': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f"{BASE_DIR}/../logs/errors.log",
                'formatter': 'default',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 5
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'django', 'errors'],
                'level': 'INFO'
            },
            'api': {
                'handlers': ['console', 'caster_dashboard', 'errors'],
                'level': 'INFO'
            },
            'caster_dashboard_2': {
                'handlers': ['console', 'caster_dashboard', 'errors'],
                'level': 'INFO'
            },
            'dashboard': {
                'handlers': ['console', 'caster_dashboard', 'errors'],
                'level': 'INFO'
            },
            'overlays': {
                'handlers': ['console', 'caster_dashboard', 'errors'],
                'level': 'INFO'
            },
            'websockets': {
                'handlers': ['console', 'caster_dashboard', 'errors'],
                'level': 'INFO'
            },
        }
    }

# endregion
