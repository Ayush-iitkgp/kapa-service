import os

import django
import pytest
from rest_framework.test import APIClient

from org.models import Project, ProjectAPIKey, Team


@pytest.fixture
def team() -> Team:
    yield Team.objects.create(name="Test Team")


@pytest.fixture
def project(team: Team) -> Project:
    yield Project.objects.create(team=team)


@pytest.fixture
def api_key(project: Project):
    yield ProjectAPIKey.objects.create(project=project)


@pytest.fixture
def client_api_token(api_key: ProjectAPIKey) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_X_API_KEY=api_key.hashed_key)
    yield client


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()
