"""
    Settings only used for Github CI testing
    DO NOT use this configuration in production!
"""

from caster_dashboard_2.settings.base import *

# Disable in production
DEBUG = True

# Keep this secret - Set individually for each host
# You can use the get_random_secret_key() function from django.core.management.utils to generate a secret key
SECRET_KEY = '^rt%q)^*ejq4qx6c3ulm%o(j%o-sd@rw)*-4n$zp4y&z^8tciw'

# Set your local database configuration here
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'caster_dashboard_2',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Static settings
# Uncomment STATIC_ROOT and comment out STATICFILES_DIRS in production
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
