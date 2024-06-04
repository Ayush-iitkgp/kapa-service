from celery import shared_task
from celery.utils.log import get_task_logger

from query.models import QuestionAnswer
from query.services.thread_classification_service import ThreadClassificationService
from query.src.email_report import EmailReportGenerator

logger = get_task_logger(__name__)


@shared_task
def send_weekly_email_report() -> None:
    """
    Sends periodic email report.
    """
    generator = EmailReportGenerator()
    generator.send_reports()


@shared_task
def classify_thread(question_answer_id: str) -> None:
    logger.info(
        f"classify_thread job started for the Question Answer {question_answer_id}"
    )
    try:
        question_answer = QuestionAnswer.objects.get(id=question_answer_id)
        thread = question_answer.thread
        ThreadClassificationService.classify(thread)
    except QuestionAnswer.DoesNotExist:
        logger.error(f"Question Answer {question_answer_id} does not exist")
