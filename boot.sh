#! /bin/sh
python manage.py compilemessages
python manage.py collectstatic --noinput
exec gunicorn type_one.wsgi:application --bind 0.0.0.0:$PORT --log-file -