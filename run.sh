#!/bin/bash
set -e

cd web
npm run serve &
cd ../sandbox
python manage.py runserver
