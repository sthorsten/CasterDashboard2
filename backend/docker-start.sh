#!/bin/bash

mkdir -p logs
mkdir -p static
mkdir -p media

# Wait 5s. for the postgres container to be up and running
sleep 5

. .venv/bin/activate
cd src
python3 manage.py migrate
python3 manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8000 caster_dashboard_2.asgi:application