#!/bin/bash

python manage.py makemigrations
python manage.py migrate

python manage.py checkdb

python manage.py test