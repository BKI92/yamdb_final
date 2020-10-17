API YAMDB
![yamdb_workflow Actions Status](https://github.com/BKI92/yamdb_final/workflows/yamdb_workflow/badge.svg)
Сервис для хранения базы данных об отзывах, фильмах, музыке

Getting Started
# Создайте .env с настройками для подключения к БД
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=Имя БД
- POSTGRES_USER=пользователь
- POSTGRES_PASSWORD=пароль
- DB_HOST=db
- DB_PORT=5432
- запуск проекта выполняется командой <docker-compose up>
# следующий шаги
 - открываем терминал <docker exec -it web bash>
 - миграция <python manage.py migrate>
 - создание администратора <python manage.py createsuperuser>

Built With
DRF - Django Rest Framework

Versioning
На данный момент версия проекта v1. Чтобы узнать доступные версии смотрите теги в этом репозитории.

Authors
Balashov Konstantin



Acknowledgments
Спасибо, всем кто воспользовался данным сервисом, буду рад обратной связи.