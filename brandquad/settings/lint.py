from .base import Base


class Lint(Base):

    PROJECT_ENVIRONMENT = "lint"

    DEBUG = True
    ALLOWED_HOSTS = ["*"]

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    SECRET_KEY = "xxx"  # noqa: S105
