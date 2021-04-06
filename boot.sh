python manage.py compilemessages
python manage.py collectstatic --noinput
exec gunicorn type_one.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers=3 --threads=3 --worker-connections=1000 --log-file -