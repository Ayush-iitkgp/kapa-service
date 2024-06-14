import logging

from query.models import Thread
from query.src.classifier_agent import ClassifierAgent

logger = logging.getLogger(__name__)


class ThreadClassificationService:
    @classmethod
    def classify(cls, thread: Thread) -> None:
        project = thread.project
        first_question_answer = thread.question_answers.order_by("created_at").first()
        classifier_agent = ClassifierAgent(project=project)
        label = classifier_agent.classify_question(first_question_answer.question)
        thread.update_label(label=label)
