#!/bin/sh
set -e

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput --clear

just reset-db
just seed
just create-su

exec uv run gunicorn main.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
