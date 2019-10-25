#!/bin/bash
set -e

pip install -r requirements.txt
docker pull python:3.7
cd web
npm install

cd ../sandbox
python manage.py migrate
python manage.py createsuperuser
