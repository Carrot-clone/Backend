#!/bin/bash

REPOSITORY=/home/ubuntu/django/Backend
cd $REPOSITORY

source /home/ubuntu/django/venv/bin/activate

export DJANGO_SECRET_KEY=${{ secrets.SECRET_KEY }}
export AWS_ACCESS_KEY=${{ secrets.AWS_ACCESS_KEY }}
export AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}
export RDS_NAME=${{ secrets.RDS_NAME }}
export RDS_USER=${{ secrets.RDS_USER }}
export RDS_PWD=${{ secrets.RDS_PWD }}
export RDS_HOST=${{ secrets.RDS_HOST }}

python3 manage.py makemigrations post user

bash /home/ubuntu/restart.sh