# YaMDb
### Описание
Проект **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
### Технологии
Python 3.8.5  
Django 3.0.5  
Django REST framework 3.11.0  
Docker 3.8
### Запуск проекта в Docker-контейнерах
- Установите [Docker](https://www.docker.com/get-started)
- Клонируйте репозиторий:
```bash
git clone https://github.com/roman-rykov/infra_sp2
```
- Перейдите в папку с проектом:
```bash
cd infra_sp2
```
- Создайте файл `.env`
```bash
touch .env
```
- Запишите в `.env` следующее содержимое
```bash
DJANGO_SECRET_KEY=mydjangosecretkey # Измените это
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mypostgrespassword # Измените это
DB_HOST=db
DB_PORT=5432

```
- Cоберите и запустите контейнеры:
```bash
docker-compose up
```
- В новом окне терминала перейдите в папку с проектом, выполните миграции, заполните базу тестовыми данными и создайте суперпользователя:
```bash
# Выполнение миграций
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
# Перенос статических файлов
docker-compose exec web python manage.py collectstatic --noinput 
# Заполнение базы данных
docker-compose exec web python manage.py loaddata fixtures.json --noinput
# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
```
- Проект станет доступен по адресу http://127.0.0.1/
### Использование
Подробная документация доступна по адресу http://127.0.0.1/redoc/  
Web-интерфейс для API http://127.0.0.1/api/v1/titles/
### Авторы
Артем Богатов, Роман Рыков, Александр Фролов
