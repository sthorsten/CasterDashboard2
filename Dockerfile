############
# Frontend #
############

FROM node:lts-alpine as frontend-build

WORKDIR /app

# Install node dependencies
COPY ./frontend/package*.json ./
RUN npm install

# Copy frontend files and override with production config
COPY ./frontend .
COPY ./frontend/vue.config.prod.js ./vue.config.js
COPY ./frontend/src/main.prod.js ./src/main.js
COPY ./frontend/src/router/index.prod.js ./src/router/index.js

RUN npm run build

# Move asset files
RUN mv ./dist/assets/* ./dist

###########
# Backend #
###########

FROM python:3.8-alpine

WORKDIR /opt/caster_dashboard_2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev python3-dev gcc musl-dev libressl-dev libffi-dev zlib-dev jpeg-dev libwebp-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Copy frontend files
COPY --from=frontend-build /app/dist ./assets

# Copy overrides
COPY ./caster_dashboard_2/settings/base.prod.py ./caster_dashboard_2/settings/base.py
#COPY ./docker-settings.py ./dashboard/settings.py => Needs to be loaded externally