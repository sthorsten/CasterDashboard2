#!/bin/bash
mkdir /backend/logs
touch /backend/logs/django.log
touch /backend/logs/dashboard.log

# Wait 5s. for the db container to be up and running
sleep 5

python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
daphne -b 0.0.0.0 -p 8000 caster_dashboard_2.asgi:application