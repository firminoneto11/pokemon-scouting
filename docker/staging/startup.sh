#!/bin/bash

set -e

echo "Running migrations..."

alembic upgrade head;

echo "Done!"

echo "Starting server..."

python3 manage.py runserver;
