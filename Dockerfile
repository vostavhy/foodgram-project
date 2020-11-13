FROM python:3.8.5-alpine

RUN apk update\
	&& apk add postgresql postgresql-contrib python3-dev musl-dev\
	&& apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev\
	&& apk add jpeg-dev zlib-dev libjpeg\
	&& pip install --upgrade pip

WORKDIR /app
COPY ./ ./

RUN pip install -r requirements.txt
