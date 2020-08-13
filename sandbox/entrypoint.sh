#!/bin/bash
set -e
pip install -r /requirements.txt
python manage.py migrate
echo 'import initial_demo' | python manage.py shell
python -u manage.py runserver 0.0.0.0:8000
