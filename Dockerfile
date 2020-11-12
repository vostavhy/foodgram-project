# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.8.5-alpine

# обновить ОС, обновить её и установить необходимые библиотеки
RUN apk update\
	&& apk add postgresql postgresql-contrib python3-dev musl-dev\
	&& apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev\
	&& apk add jpeg-dev zlib-dev libjpeg\
	&& pip install --upgrade pip

# создать папку, назначить её рабочей дирреторией и скопировать туда всё из текущей папки
WORKDIR /app
COPY ./ ./

# установить все зависимости
RUN pip install -r requirements.txt

# run entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]
