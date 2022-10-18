#!/bin/sh
set -ex

python manage.py reset_db --noinput
python manage.py makemigrations --no-header
python manage.py migrate
python manage.py makedemo
