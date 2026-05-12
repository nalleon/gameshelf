#!/bin/sh
set -e

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput --clear

exec uv run gunicorn main.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
