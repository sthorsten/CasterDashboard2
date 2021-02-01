############
# Frontend #
############

#FROM node:lts-alpine as frontend-build

#WORKDIR /frontend

# Install node dependencies
#COPY ./frontend/package.json ./
#RUN yarn install

# Copy frontend files and set docker .env file
#COPY ./frontend .
#COPY ./frontend/.env.docker ./.env

# Generate static nuxt site
#RUN yarn generate -- --devtools

###########
# Backend #
###########

FROM python:3.8-alpine

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev python3-dev gcc musl-dev libressl-dev libffi-dev zlib-dev jpeg-dev libwebp-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Copy frontend files
#COPY --from=frontend-build /frontend/dist /frontend

# Copy environment file
COPY .env.docker ./.env