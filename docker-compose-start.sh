#!/bin/bash
python3 manage.py migrate --settings=dashboard.settings
python3 manage.py collectstatic --settings=dashboard.settings --noinput --clear
daphne -b 0.0.0.0 -p 8000 dashboard.asgi:application
