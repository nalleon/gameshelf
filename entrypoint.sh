#!/bin/sh
set -e

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput --clear

if [ ! -f /app/data/.init_done ]; then
  just makemigrations
  just migrate
  just seed
  just create-su
  touch /app/data/.init_done
fi

exec "$@"
