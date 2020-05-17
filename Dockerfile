FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY manage.py /code/
COPY requirements.txt /code/
COPY type_one /code/
RUN pip install -r requirements.txt
CMD exec gunicorn type_one.wsgi:application --bind 0.0.0.0:$PORT --log-file -