"""
Logging settings file

This file specifies the host-specific logging settings on where and how to log program actions
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s.%(msecs)03d] %(levelname)s [%(name)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'formatter': 'verbose',
        },
        'caster_dashboard': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'caster_dashboard.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'formatter': 'verbose',
        }

    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'caster_dashboard_2': {
            'handlers': ['caster_dashboard'],
            'level': 'DEBUG',
        },
        'dashboard': {
            'handlers': ['caster_dashboard'],
            'level': 'DEBUG',
        },
        'overlays': {
            'handlers': ['caster_dashboard'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['caster_dashboard'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}
