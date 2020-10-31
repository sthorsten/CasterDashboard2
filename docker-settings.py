# Do not change!
from caster_dashboard_2.settings.base import *

# Disable in production
DEBUG = True

# Keep this secret - Set individually for each host
# You can use the get_random_secret_key() function from django.core.management.utils to generate a secret key
SECRET_KEY = ''

# Email settings
DEFAULT_FROM_EMAIL = 'mail@example.com'
EMAIL_SUBJECT_PREFIX = '[Caster Dashboard] '
EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
