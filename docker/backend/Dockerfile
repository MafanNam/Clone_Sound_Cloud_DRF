# pull official base image
FROM python:3.11-alpine3.15
LABEL maintainer="Mafan"

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./clone_sound_cloud /app/clone_sound_cloud
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
RUN chmod +x /app/docker/backend/celery-beat-entrypoint.sh
