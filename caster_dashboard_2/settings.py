"""
    Base settings for the Django Backend
"""

import os
from datetime import timedelta
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
    'widget_tweaks',
    'channels',
    'corsheaders',
    'dashboard.apps.DashboardConfig',
    'overlays.apps.OverlaysConfig',  # Deprecated
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
    'caster_dashboard_2.argon2id.Argon2idPasswordHasher',  # temporary until release of Django 3.2
    # 'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher'  # Fallback
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

# endregion

# region REST Framwork / Authentication

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # deprecated
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer', 'Token',)
}

# Prevent client-side javscript from accessing the token
# to prevent axios from sending the cookie in POST requests
CSRF_COOKIE_HTTPONLY = True

# endregion

#region Logging

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s.%(msecs)03d] %(levelname)s [%(name)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

        # File Handlers
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },

        'dashboard_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'dashboard.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'caster_dashboard_2': {
            'handlers': ['console', 'dashboard_file'],
            'level': 'DEBUG',
        },
        'dashboard': {
            'handlers': ['console', 'dashboard_file'],
            'level': 'DEBUG',
        },
        'overlays': {
            'handlers': ['console', 'dashboard_file'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['console', 'dashboard_file'],
            'level': 'DEBUG',
        },
        'websockets': {
            'handlers': ['console', 'dashboard_file'],
            'level': 'DEBUG',
        }
    },
}
"""

#endregion

# region DEPRECATED - soon to be removed
# Will be handled by the Vue / Nuxt frontend

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'caster_dashboard_2.context_processors.version_context',
                'caster_dashboard_2.context_processors.profile_context',
            ],
        },
    },
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
)

# endregion

# region USER / HOST CONFIG SECTION

# Read from environment file
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

DEBUG = env('DEBUG', cast=bool)
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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

if env('MODE') == 'production':
    STATIC_ROOT = os.path.join(BASE_DIR, "assets")

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Allowed Hosts / Origins
# Includes localhost and the internal docker network ("dashboard") by default

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'backend',
    'frontend'
]

ALLOWED_HOSTS = ALLOWED_HOSTS + env('ALLOWED_HOSTS', cast=[str])
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

print(CSRF_TRUSTED_ORIGINS)

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^(https?:\/\/localhost):(\d*)",
    r"^(https?:\/\/127.0.0.1):(\d*)",
    r"^(https?:\/\/backend):(\d*)",
    r"^(https?:\/\/frontend):(\d*)",
]

# Add entries from ALLOWED_HOSTS to CORS_ALLOWED_ORIGIN_REGEXES
for host in env('ALLOWED_HOSTS', cast=[str]):
    CORS_ALLOWED_ORIGIN_REGEXES.append(r"^(https?:\/\/" + host + r"):(\d*)")

# endregion
