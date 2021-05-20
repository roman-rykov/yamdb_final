[![CI](https://github.com/roman-rykov/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)](https://github.com/roman-rykov/yamdb_final/actions/workflows/yamdb_workflow.yaml)
# YaMDb
### Описание
Проект **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
### Технологии
Проект написан на Python 3.8, использует Django 3.2 и Django REST Framework 3.12 и собирается в Docker-контейнерах.
### Запуск проекта в Docker-контейнерах
- Установите [Docker](https://www.docker.com/get-started) и [Docker Compose](https://docs.docker.com/compose/install/)
- Клонируйте репозиторий:
```bash
git clone https://github.com/roman-rykov/yamdb_final
```
- Перейдите в папку с проектом:
```bash
cd yamdb_final/
```
- Переименуйте `.env.example` в `.env`:
```bash
mv .env.example .env
```
- Добавьте значения ключей `DJANGO_SECRET_KEY` и `POSTGRES_PASSWORD` в файле `.env`
- Cоберите и запустите контейнеры:
```bash
docker-compose up
```
- В новом окне терминала перейдите в папку с проектом, выполните миграции, заполните базу тестовыми данными и создайте суперпользователя:
```bash
# Выполнение миграций
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
# Перенос статических файлов
docker-compose exec web python manage.py collectstatic --noinput 
# Заполнение базы данных
docker-compose exec web python manage.py loaddata fixtures.json
# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
```
- Проект станет доступен по адресу http://127.0.0.1/
### Использование
Подробная документация доступна по адресу http://127.0.0.1/redoc/  
Web-интерфейс для API http://127.0.0.1/api/v1/titles/
### Тестовая веб-версия
Проверить работу сервиса вы можете на http://yamdb.gq/api/v1/
### Авторы
Артем Богатов, Роман Рыков, Александр Фролов.
