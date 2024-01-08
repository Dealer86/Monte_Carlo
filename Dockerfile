FROM python:3.11.4

WORKDIR /code

ENV PORT 8000

COPY . /code

RUN pip install -r requirements.txt

WORKDIR /code/montecarlo

CMD python3 manage.py runserver 0.0.0.0:8000
