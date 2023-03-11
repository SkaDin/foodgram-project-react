![](https://github.com/SkaDin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# API для проекта YaMDB в Docker-контейнере

## Описание
### Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). Сайт не предоставляет прямой доступ или ссылки для непосредственного ознакомления с произведениями.

### Проект доступен по [адресу](http://84.201.152.177/api/v1/)
P.S. Может быть недоступен в связи с прекращением обслуживания.
    
### Используемые технологии:
* [![Django](https://camo.githubusercontent.com/cbef21adebc167fac6552145a03c9e12ae03b8afd5e4f7de52379a98297de3fe/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f444a414e474f2d524553542d6666313730393f7374796c653d666f722d7468652d6261646765266c6f676f3d646a616e676f266c6f676f436f6c6f723d776869746526636f6c6f723d666631373039266c6162656c436f6c6f723d67726179)](https://www.django-rest-framework.org/)  3.12.4 
* [![Postgres](https://camo.githubusercontent.com/29e7fc6c62f61f432d3852fbfa4190ff07f397ca3bde27a8196bcd5beae3ff77/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f706f7374677265732d2532333331363139322e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d706f737467726573716c266c6f676f436f6c6f723d7768697465)](https://www.postgresql.org/) 12.2
* [![Python](https://camo.githubusercontent.com/eb61c0a4e1607e8052a9feb827408d8315a08b148089601fbe8dc3b0a8a466ff/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d507974686f6e2d3436343634363f7374796c653d666c61742d737175617265266c6f676f3d507974686f6e)](https://www.python.org/) 3.8
* [![Gunicorn](https://camo.githubusercontent.com/c88b97546b409f575bc4391a817849ef096823826d157bac9ebc80e64c82b524/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d67756e69636f726e2d3436343634363f7374796c653d666c61742d737175617265266c6f676f3d67756e69636f726e)](https://gunicorn.org/) 20.0.4
* [![nginx](https://camo.githubusercontent.com/5b86c36f70c8c587bc5c3d92b0d1a134186328d5ff3bc62fbd1ca1c592838c67/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d4e47494e582d3436343634363f7374796c653d666c61742d737175617265266c6f676f3d4e47494e58)](https://nginx.org/ru/)
* [![Docker](https://camo.githubusercontent.com/bee90761c6a7a782a6886d6104c8c6e70eb65a6e8e032ced5a9fa659a42bcaa6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d446f636b65722d3436343634363f7374796c653d666c61742d737175617265266c6f676f3d646f636b6572)](https://www.docker.com/) 20.10.23
* [![GitHub_Actions](https://camo.githubusercontent.com/3c0f7b387b2c37dde06f213314f47550a8069ab0b56df55e169fc44da490b80d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d476974487562253230416374696f6e732d3436343634363f7374796c653d666c61742d737175617265266c6f676f3d476974487562253230616374696f6e73)](https://github.com/features/actions)
* [![YaCloud](https://camo.githubusercontent.com/e9eb246dba9c31eef78da4a970347cae81f2b8121dc1eea45f0f6d23b12e058b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d59616e6465782e436c6f75642d3436343634363f7374796c653d666c61742d737175617265266c6f676f3d59616e6465782e436c6f7564)](https://cloud.yandex.ru/)
* Django 3.2
* CI и CD 


## Как запустить проект:
### Все описанное ниже относится к ОС Linux и выполняется от имени администратора. Клонируем репозиторий и переходим в него:

```
git clone git@github.com:SkaDin/yamdb_final.git
```
### Выполнить вход на удаленный сервер и установить docker на сервер: 
```
apt install docker.io 
```
### Установить docker-compose на сервер:

```
curl -SL https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```
### Отредактировать и cкопировать файлы docker-compose.yml и nginx.conf из директории infra на сервер:

```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml

scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
### Добавить в Secrets GitHub переменные окружения для работы :
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>

```
### Workflow состоит из четырёх шагов:
1. Проверка кода на соответствие PEP8.
2. Сборка и отправка образа на DockerHub.
3. Автоматический деплой на удаленный сервер.
4. Отправка уведомления в телеграм-чат.

### После успешной сборки выполнить следующие действия (только при первом деплое):
### Провести миграцию внутри контейнера(собранного из образа):
```
docker-compose exec web python manage.py migrate
```
### Собираем статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
### Создаем суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
### Заполняем базу данными

### Создаем дамп базы данных (нет в текущем репозитории):
```
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```
### Останавливаем контейнеры:
```
docker-compose down -v
```
### Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<секретный ключ проекта django>
```
### Основные используемые библиотеки:
```
asgiref==3.2.10
Django==2.2.16
django-filter==2.4.0
djangorestframework==3.12.4
djangorestframework-simplejwt==4.8.0
gunicorn==20.0.4
psycopg2-binary==2.8.6
PyJWT==2.1.0
pytz==2020.1
sqlparse==0.3.1 
```
## Автор проекта: 
SkaDin(Сушков Денис)

### Документация API YaMDb
```Документация доступна по эндпойнту: http://<IP-сервера>/redoc/ ```
