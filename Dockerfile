FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY manage.py /code/
COPY requirements.txt /code/
COPY type_one /code/type_one
COPY staticfiles /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install gettext
COPY boot.sh /code/
CMD ./boot.sh