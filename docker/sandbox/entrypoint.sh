#!/bin/bash
set -e
source ../venv/bin/activate
pip install -r ../requirements.txt
python manage.py migrate
echo 'import initial_demo' | python manage.py shell
python manage.py runserver 0.0.0.0:$PORT
