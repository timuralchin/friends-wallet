# Friends wallet

Приложение для учета собственных трат и трат в группе.

Назначение:

Пользователь может добавлять собственные чек, вести учет в рамках личных и групповых трат.

## Старт проекта

Создать `.env` файл с `.env.example` и заполнить их необходимыми значениями.

Установить зависимости:

```shell
poetry install
```

Активировать виртуальное окружения:

```shell
poetry shell
```

Накатить миграции:

```shell
python manage.py migrate
```

Создать суперпользователя для доступа к админке:

```shell
python manage.py createsuperuser
```

Запуск приложения:

```shell
python manage.py runserver
```

## Запуск линтеров

```shell
flake8 .
```

## Панель администратора

`http://localhost:8000/admin

## Схема api

`http://localhost:8000/api/v1/swagger/

## Запуск в докере

docker-compose up -d
