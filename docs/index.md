# Как проверять тестовое задание
В [README](../README.md) общее описание проекта. Здесь еще раз кратко все описано для быстрой проверки.

0. Склонировать репозиторий
```shell
git clone https://github.com/ReznikovRoman/brandquad_take_home.git && cd brandquad_take_home
```

1. Указать переменные окружения в файле `.env` в корне проекта.
```shell
cat << EOF > .env
ENV=.env
PYTHONUNBUFFERED=1
DJANGO_SETTINGS_MODULE=brandquad.settings
DJANGO_CONFIGURATION=Local
DJANGO_ADMIN=django-cadmin
SECRET_KEY=7)%31(swa1yditp7@g87_h8deqi4dj=1pjp^ysv*tnm_fxxfw6
ALLOWED_HOSTS=localhost,127.0.0.1
BQ_PROJECT_BASE_URL=http://localhost:8000
BQ_MEDIA_URL=/media/
BQ_STATIC_URL=/staticfiles/
BQ_DB_HOST=db
BQ_DB_PORT=5432
BQ_DB_NAME=brandquad
BQ_DB_USER=user
BQ_DB_PASSWORD=pswd
BQ_CI=0
EOF
```

2. Создать локальный файл конфигурации Django `brandquad/settings/local.py`. Пример:
```shell
cat << EOF > brandquad/settings/local.py
import mimetypes
import socket

from .base import Base
from .values import from_environ


class Local(Base):
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]

    STATIC_URL = "staticfiles/"

    LOG_SQL = from_environ(False, name="PROJECT_LOG_SQL", type=bool)

    # debug toolbar
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda show_toolbar: True,
    }
    mimetypes.add_type("application/javascript", ".js", True)

    DEV_INSTALLED_APPS = [
        "debug_toolbar",
    ]
    DEV_MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    Base.INSTALLED_APPS.extend(DEV_INSTALLED_APPS)
    Base.MIDDLEWARE.extend(DEV_MIDDLEWARE)
EOF
```

3. Запустить докер контейнеры
```shell
docker-compose build
docker-compose up -d
```

4. Запустить management команду `import_nginx_logs` и дождаться её выполнения.
Вместо указанной ссылки можно использовать любую другую, ведущую на файл в нужном формате (например, на файл на S3).
```shell
docker-compose run --rm server sh -c 'django-cadmin import_nginx_logs https://gist.githubusercontent.com/ReznikovRoman/f38befcf3a8b779e65a16306dafbe536/raw/6c32ac9892e7bb9ef37df6b4d42acc8108a7365b/brandquad_nginx_logs_huge.txt'
```

5. Зайти в админ. панель по адресу `http://localhost:8000/admin/observability/nginxlog/`.
Доступы от админки указаны в докер композе:
```dotenv
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=pass
```

6. Зайти в [Swagger для
проверки АПИ](http://localhost:8000/api/v1/schema/swagger#/observability/observability_nginx_logs_list) или сделать curl запрос:
```shell
curl -X 'GET' \
  'http://localhost:8000/api/v1/observability/nginx/logs' \
  -H 'accept: application/json'
```

7. После проверок остановить контейнеры и удалить все лишние данные
```shell
docker-compose down -v --remove-orphans --rmi local
```
