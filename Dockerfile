FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY manage.py /code/
COPY requirements.txt /code/
COPY type_one /code/type_one
COPY staticfiles /code/
COPY setup.sh /code/