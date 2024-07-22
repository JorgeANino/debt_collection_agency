#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -w 1 $DB_HOST $DB_PORT; do
      echo "Waiting for PostgreSQL to start..."
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000