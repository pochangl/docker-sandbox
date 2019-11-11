#!/bin/bash
set -e
source ../venv/bin/activate
pip install -r ../requirements.txt

daphne sandbox.asgi:application --port $PORT --bind 0.0.0.0 -v2
