#!/bin/bash
set -e

pip install -r requirements.txt
docker pull python:latest
cd web
npm install

cd ../sandbox
python manage.py migrate
python manage.py createsuperuser
