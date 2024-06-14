import pytest

from query.models import Project, QuestionAnswer, Thread
from query.services.thread_classification_service import ThreadClassificationService

pytestmark = pytest.mark.django_db


def test_thread_classification_service_success(
    question_answer: QuestionAnswer, thread: Thread, project: Project
):
    ThreadClassificationService.classify(thread)
    thread.refresh_from_db()
    assert thread.label in project.labels
