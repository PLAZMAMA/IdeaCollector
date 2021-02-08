FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --no-input --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install

ADD . /code/
