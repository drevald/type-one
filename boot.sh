python manage.py compilemessages --locale ru_RU
python manage.py compilemessages --locale en_EN
python manage.py collectstatic --noinput
python manage.py migrate
exec gunicorn type_one.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers=3 --threads=3 --worker-connections=1000 --log-file -