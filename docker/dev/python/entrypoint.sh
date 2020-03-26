#!/bin/bash

python /code/manage.py makemigrations
python /code/manage.py migrate

echo "Running command '$*'"
exec /bin/bash -c "$*"
