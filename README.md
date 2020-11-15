# foodgram-project. Дипломный проект курса python developer от Yandex Praktikum
сайт доступен по адресу http://84.201.162.40/

![Build Status](https://github.com/vostavhy/foodgram-project/workflows/foodgram/badge.svg)

## Установка

#### Шаг первый. Установка Docker и docker-compose
Для установки воспользуйтесь официальной [инструкцией](https://docs.docker.com/engine/install/).

#### Шаг второй. Установка переменных окружения
в папке foodgram создайте файл .env с следующим содержанием (значения переменных приведены для примера):
```bash
DB_ENGINE=django.db.backends.postgresql
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_pass

SECRET_KEY=&*eziv-@m%+)!ptxv4&2%b_&asw32rkfsc9b)9h4k9wfze=fn-@z65%(czasdfa
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] 
```

#### Шаг третий. Сборка и запуск контейнера
```bash
docker-compose up -d --build
```
#### Шаг четвертый. База данных
```bash
docker-compose run web python manage.py makemigrations --no-input
docker-compose run web python manage.py migrate --no-input
docker-compose run web python manage.py loaddata fixtures.json
```

## Использование
### Запуск контейнеров
```bash
docker-compose up
```

### Выключение контейнеров
```bash
docker-compose down
```
