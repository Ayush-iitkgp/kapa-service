import pytest

from org.models import Project
from query.models import Thread


@pytest.fixture
def thread(project: Project) -> Thread:
    yield Thread.objects.create(project=project)
