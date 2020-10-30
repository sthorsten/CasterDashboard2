"""

    Base Django settings file of the project

"""



import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.thorshero.de']



WSGI_APPLICATION = 'caster_dashboard_2.routing.application'

ASGI_APPLICATION = 'caster_dashboard_2.routing.application'



# Application definition

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

    'overlays.apps.OverlaysConfig',

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



# Database config

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'caster_dashboard_2',

        'USER': 'caster_dashboard_2',

        'PASSWORD': 'caster_dashboard_2',

        'HOST': 'db',

        'PORT': '5432',

    }

}





# URL configuration

ROOT_URLCONF = 'caster_dashboard_2.urls'

LOGIN_URL = '/login'



TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [os.path.join(BASE_DIR, 'frontend/dist')]

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



LOCALE_PATHS = (

    os.path.join(BASE_DIR, 'locale'),

)



LANGUAGES = (

    ('en', 'English'),

    ('de', 'German'),

)



# Static settings

# Uncomment STATIC_ROOT and comment out STATICFILES_DIRS in production

STATIC_URL = '/assets/'

STATIC_ROOT = os.path.join(BASE_DIR, "assets")

STATICFILES_DIRS = [

    os.path.join(BASE_DIR, "static"),

    os.path.join(BASE_DIR, "frontend", "dist")

]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")



# Django REST framework

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework.authentication.TokenAuthentication',

        'rest_framework.authentication.SessionAuthentication'

    ),

    'DEFAULT_PERMISSION_CLASSES': [

        'rest_framework.permissions.IsAuthenticated'

    ],

    'DEFAULT_FILTER_BACKENDS': [

        'django_filters.rest_framework.DjangoFilterBackend'

    ]

}



CSRF_TRUSTED_ORIGINS = [

    'localhost',

    '127.0.0.1'

]



# CORS Headers

CORS_ALLOWED_ORIGINS = [

    'http://127.0.0.1',

    'http://localhost',

    'http://127.0.0.1:8080',

    'http://localhost:8080'

]