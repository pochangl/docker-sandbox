#!/bin/bash
set -e

pip install -r requirements.txt
docker pull python:latest
cd web
npm install
