#!/bin/sh

until cd /app/clone_sound_cloud
do
    echo "Waiting for server volume..."
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

# run a worker celery beat :)
celery -A config beat -l info
