#!/bin/sh

python3 manage.py flush --no-input
python3 manage.py migrate
python3 manage.py site_management
python3 manage.py configurations
python3 manage.py administrator_panels
python3 manage.py collectstatic --noinput

exec "$@"