#!/bin/bash

cd test_task_ns

cd app

alembic upgrade head

python clear_database.py

python create_roles.py

python create_users.py

gunicorn main:application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000