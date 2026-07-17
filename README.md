Контрольная работа: приложение Blog написанное на DRF (django rest framework).
Функционал:
Регистрация и аутентификация (Token);
CRUD постов (авторизация владельца);
Система комментариев к постам;
Документация API.
Запуск:
git clone <https://github.com/what-is-lav/blog/edit/main/>
cd blog_api
pip install -r requirements.txt
Применить миграции:
python manage.py migrate
Запустить сервер:
python manage.py runserver
API Документация
После запуска проекта перейдите по адресу:http://127.0.0.1:8000/swagger/
