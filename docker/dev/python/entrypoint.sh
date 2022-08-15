#!/bin/bash

python /code/manage.py makemigrations
python /code/manage.py migrate
python /code/manage.py loaddata dealer cashback_rules

echo "Running command '$*'"
exec /bin/bash -c "$*"
