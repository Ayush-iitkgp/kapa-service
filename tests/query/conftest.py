import pytest
from rest_framework.test import APIClient

from org.models import Project, ProjectAPIKey, Team
from query.models import QuestionAnswer, Thread


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


@pytest.fixture
def thread(project: Project) -> Thread:
    yield Thread.objects.create(project=project)


@pytest.fixture()
def question_answer(thread: Thread) -> QuestionAnswer:
    yield QuestionAnswer.objects.create(
        question="random question", answer="random answer", thread=thread
    )
