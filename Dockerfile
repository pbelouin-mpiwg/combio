FROM python:3.10-slim-buster
LABEL maintainer="ronmarti18@gmail.com"

RUN apt update && apt install -y build-essential gettext python3-dev
RUN pip install -U poetry pip setuptools
RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN npm install
RUN npm i -g n
RUN n latest

ENV PYTHONUNBUFFERED=1
ENV TAILWIND_CSS_PATH=/code/static/

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN poetry config virtualenvs.create false
RUN poetry install
