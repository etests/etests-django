#!/bin/sh
set -e

mkdir -p static
python manage.py migrate --noinput
python manage.py collectstatic --no-input

exec "$@"