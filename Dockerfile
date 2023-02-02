# syntax=docker/dockerfile:1
FROM python:3.10-alpine

ENV MY_HOUSE_24=/home/app/my_house_24

RUN mkdir -p $MY_HOUSE_24

WORKDIR $MY_HOUSE_24

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY ./entrypoint.sh $MY_HOUSE_24/

RUN sed -i 's/\r$//g' $MY_HOUSE_24/entrypoint.sh
RUN chmod +x $MY_HOUSE_24/entrypoint.sh
RUN pip install --upgrade pip

# copy project
COPY . $MY_HOUSE_24

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install -r $MY_HOUSE_24/requirements.txt

ENTRYPOINT ["/home/app/my_house_24/entrypoint.sh"]