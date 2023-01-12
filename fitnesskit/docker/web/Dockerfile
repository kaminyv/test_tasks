# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./api_gateway/requirements.txt .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --skip-checks --noinput
