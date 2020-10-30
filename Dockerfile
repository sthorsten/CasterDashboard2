FROM python:3.8-alpine

WORKDIR /opt/caster_dashboard_2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev python3-dev gcc musl-dev libressl-dev libffi-dev zlib-dev jpeg-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy all project files (exceptions: .dockerignore)
COPY . .

# Copy Compui
COPY ./frontend/dist/assets ./frontend/dist
COPY ./frontend/dist/favicon.ico ./frontend/dist
COPY ./frontend/dist/index.html ./frontend/dist


COPY . .

# Copy production base config
COPY ./caster_dashboard_2/settings/base.prod.py ./caster_dashboard_2/settings/base.py
