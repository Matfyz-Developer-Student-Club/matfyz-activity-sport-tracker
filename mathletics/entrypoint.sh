#!/usr/bin/env bash

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ "$FLASK_ENV" = "development" ]
then
  echo "Creating the database tables..."
  python -u manage.py create_db
  echo "Tables created."
fi

exec "$@"