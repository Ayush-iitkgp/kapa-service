import pytest

from org.models import Project
from query.models import BackFillStatus, QuestionAnswer, Thread


@pytest.fixture
def thread(project: Project) -> Thread:
    yield Thread.objects.create(project=project)


@pytest.fixture()
def question_answer(thread: Thread) -> QuestionAnswer:
    yield QuestionAnswer.objects.create(
        question="random question", answer="random answer", thread=thread
    )


@pytest.fixture()
def back_fill_status(thread: Thread) -> BackFillStatus:
    yield BackFillStatus.objects.create(thread=thread, is_back_filled=False)
