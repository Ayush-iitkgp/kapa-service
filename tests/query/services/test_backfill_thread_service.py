import pytest

from query.models import BackFillStatus, Project, QuestionAnswer, Thread
from query.services.backfill_thread_service import BackFillThreadService

pytestmark = pytest.mark.django_db


def test_thread_classification_service_success(
    back_fill_status: BackFillStatus,
    question_answer: QuestionAnswer,
    thread: Thread,
    project: Project,
):
    assert thread.label is None
    assert back_fill_status.is_back_filled is False
    BackFillThreadService.back_fill_thread(thread)
    thread.refresh_from_db()
    back_fill_status.refresh_from_db()
    assert thread.label is not None
    assert back_fill_status.is_back_filled is True
