# syntax=docker/dockerfile:1
FROM python:3.10

ENV MY_HOUSE_24=/home/app/my_house_24

RUN mkdir -p $MY_HOUSE_24

WORKDIR $MY_HOUSE_24

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY . $MY_HOUSE_24

RUN apt-get update
RUN apt-get upgrade -y && apt-get -y install gcc python3-dev wkhtmltopdf locales

RUN sed -i '/uk_UA.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG uk_UA.UTF-8
ENV LANGUAGE uk_UA:uk
ENV LC_ALL uk_UA.UTF-8

RUN pip install -r requirements.txt
