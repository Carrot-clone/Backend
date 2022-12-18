#!/bin/bash

REPOSITORY=/home/ubuntu/django/Backend
cd $REPOSITORY

source /home/ubuntu/django/venv/bin/activate

sudo systemctl restart gunicorn
sudo systemctl restart nginx