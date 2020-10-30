# Do not change!
from caster_dashboard_2.settings.base import *

# Disable in production
DEBUG = True

# Keep this secret - Set individually for each host
# You can use the get_random_secret_key() function from django.core.management.utils to generate a secret key
SECRET_KEY = 'ffo6!d+2mr)7o8w8&2jcmrm500f6es%yonn82hckxigco-=(nl'

# Email settings
DEFAULT_FROM_EMAIL = 'noreply@thorshero.de'
EMAIL_SUBJECT_PREFIX = '[Caster Dashboard] '
EMAIL_HOST = 'mail.tschmitt.eu'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mail@tschmitt.eu'
EMAIL_HOST_PASSWORD = 'klV5yIDx64tp2EG6VFkE'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
