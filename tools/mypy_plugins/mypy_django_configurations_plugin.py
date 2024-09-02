import os

from configurations import importer
from mypy_django_plugin import main
from mypy_django_plugin.main import NewSemanalDjangoPlugin


def plugin(version: str) -> type[NewSemanalDjangoPlugin]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandquad.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Lint")
    importer.install()
    return main.plugin(version)
