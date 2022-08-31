#!/bin/sh
set -ex

# TODO: After migrations are under version control, remove this.
rm -f example_app/migrations/00[0-9][0-9]_*.py

python manage.py reset_db --noinput
python manage.py makemigrations --no-header
python manage.py migrate
# TODO: python manage.py makedemo
