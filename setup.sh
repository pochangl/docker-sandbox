#!/bin/bash

pip install -r requirements.txt
docker pull python:latest
cd web
npm install
