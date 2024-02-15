#!/bin/sh

cd /home/app/web

python manage.py migrate
python manage.py loaddata fixture.json
python manage.py admin_fixture
gunicorn core.wsgi -b 0.0.0.0:8000


# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# # python manage.py flush --no-input
# # python manage.py migrate
# # python manage.py loaddata fixture.json
# # python manage.py runserver 0.0.0.0:8000

# exec "$@"