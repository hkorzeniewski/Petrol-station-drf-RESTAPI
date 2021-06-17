FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000


