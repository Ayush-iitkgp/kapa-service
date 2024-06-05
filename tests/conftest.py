import os

import django
import pytest
from rest_framework.test import APIClient


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
    django.setup()


pytest_configure()

from org.models import Project, ProjectAPIKey, Team  # noqa: E402


@pytest.fixture
def team() -> Team:
    yield Team.objects.create(name="Test Team")


@pytest.fixture
def project(team: Team) -> Project:
    yield Project.objects.create(team=team)


@pytest.fixture
def api_key(project: Project) -> ProjectAPIKey:
    project_api_key, key = ProjectAPIKey.objects.create_key(name="Test API Key")
    project_api_key.projects.add(project)
    yield key


@pytest.fixture
def client_api_token(api_key: str) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_X_API_KEY=api_key)
    yield client
