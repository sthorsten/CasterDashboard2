"""
Database settings file

This file specifies the host-specific database settings which the program should use
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'caster_dashboard_2',
        'USER': 'caster_dashboard_2',
        'PASSWORD': 'caster_dashboard_2',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
