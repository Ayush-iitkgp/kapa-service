import pytest

from query.tasks import classify_thread

pytestmark = pytest.mark.django_db


def test_classify_thread(question_answer) -> None:
    thread = question_answer.thread
    assert thread.label is None
    classify_thread.apply(
        throw=True, kwargs={"question_answer_id": str(question_answer.id)}
    )
    question_answer.refresh_from_db()
    thread = question_answer.thread
    assert thread.label is not None
