FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install pipenv
RUN echo "PASSED1"
COPY Pipfile Pipfile.lock /code/
RUN echo "PASSED2"
RUN pipenv install
RUN echo "PASSED3"

COPY . /code/
