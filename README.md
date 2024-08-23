# Brandquad
Сервис по обработке логов Nginx для Brandquad.

## Настройка и запуск
Docker конфигурации содержат контейнеры:
1. db
2. server

Файлы docker-compose:
 1. `docker-compose.yml` - для локальной разработки.

Для успешного запуска необходимо указать переменные окружения в файле `.env` в корне проекта.

**Формат `.env` файла:**
```dotenv
ENV=.env

# Python
PYTHONUNBUFFERED=1

# Brandquad
# Django
DJANGO_SETTINGS_MODULE=brandquad.settings
DJANGO_CONFIGURATION=Local
DJANGO_ADMIN=django-cadmin
SECRET_KEY=7)%31(swa1yditp7@g87_h8deqi4dj=1pjp^ysv*tnm_fxxfw6
ALLOWED_HOSTS=localhost,127.0.0.1

# Project
BQ_PROJECT_BASE_URL=http://localhost:8000

# Media
BQ_MEDIA_URL=/media/
BQ_STATIC_URL=/staticfiles/

# Postgres
BQ_DB_HOST=db
BQ_DB_PORT=5432
BQ_DB_NAME=brandquad
BQ_DB_USER=user
BQ_DB_PASSWORD=pswd

# Config
BQ_CI=0
```

Для локальной конфигурации также необходимо создать файл конфигурации Django `brandquad/settings/local.py`. Пример:
```python
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
```

Доступы от администратора в админ. панель по умолчанию. Сама страница будет доступна по адресу `http://localhost:8000/admin:
```dotenv
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=pass
```

**Запуск производится в два этапа:**
```shell
docker-compose build
docker-compose up
```

При старте gunicorn контейнера выполняется применение миграций и сбор статики.

Перезапуск контейнеров вручную происходит в один этап:

```
docker-compose restart
```

В проекте используется [`django-configurations`](https://django-configurations.readthedocs.io/en/latest/), поэтому для выполнения management команд Django вместо `./manage.py` / `python -m django` / `django-admin` следует использовать `django-cadmin`.

## Разработка
Синхронизировать окружение с `requirements.txt` / `requirements.dev.txt` (установит отсутствующие пакеты, удалит лишние, обновит несоответствующие версии):

```shell
make sync-requirements
```

Перегенерировать `requirements.txt` / `requirements.dev.txt` (требуется после изменений в `requirements.in` / `requirements.dev.in`):

```shell
make compile-requirements
```

Если в окружении требуется установить какие-либо пакеты, которые нужно только локально разработчику, то следует создать файл `requirements.local.in` и указывать зависимости в нём. Обязательно следует указывать constraints files (`-c ...`). Например, чтобы запускать `shell_plus` c `ptipython` (`django-cadmin shell_plus --ptipython`), нужно поставить пакеты `ipython` и `ptpython`, в таком случае файл `requirements.local.in` будет выглядеть примерно так (первые строки одинаковы для всех, остальное — зависимости для примера):

```shell
-c requirements.txt
-c requirements.dev.txt

ipython >=7, <8
ptpython >=3, <4
```


### Code style:
Локальная настройка pre-commit:

```shell
pre-commit install
```

Перед пушем коммита следует убедиться, что код соответствует принятым стандартам и соглашениям:

```shell
make lint
```

Автоматически исправить возможные ошибки:

```shell
make fix
```

## Документация API
Документация в формате OpenAPI 3 доступна по адресу:

* `${PROJECT_BASE_URL}/api/v1/schema` (YAML или JSON, выбор через content negotiation заголовком `Accept`)
* `${PROJECT_BASE_URL}/api/v1/schema/redoc` (ReDoc)
* `${PROJECT_BASE_URL}/api/v1/schema/swagger` (Swagger UI)
