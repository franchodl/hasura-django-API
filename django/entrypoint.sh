#!/bin/bash -x

echo "Ensuring dependancies are up-to-date..."
pip install -r requirements.txt
echo "Migrating DB..."
python manage.py migrate --noinput || exit 1
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Initializing with default variables..."
python manage.py init
echo "Starting server"
python manage.py runserver 0.0.0.0:8000