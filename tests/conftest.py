import os

import django


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
    django.setup()


pytest_configure()
