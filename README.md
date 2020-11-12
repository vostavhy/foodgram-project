# foodgram-project. Дипломный проект курса python developer от Yandex Praktikum

![Build Status](https://github.com/vostavhy/foodgram-project/workflows/foodgram/badge.svg)

## Установка

#### Шаг первый. Установка Docker и docker-compose
Для установки воспользуйтесь официальной [инструкцией](https://docs.docker.com/engine/install/).

#### Шаг второй. Сборка и запуск контейнера
```bash
docker-compose up -d --build
```
#### Шаг третий. База данных
```bash
docker-compose run web python manage.py makemigrations --no-input
docker-compose run web python manage.py migrate --no-input
docker-compose run web python manage.py loaddata fixtures.json
```

## Использование
### Запуск контейнера
```bash
docker-compose up
```

### Выключение контейнера
```bash
docker-compose down
```
