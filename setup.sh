pip install -r requirements.txt
apt-get update
apt-get -y install gettext
python manage.py compilemessages
python manage.py collectstatic --noinput
gunicorn type_one.wsgi:application --bind 0.0.0.0:$PORT --log-file -