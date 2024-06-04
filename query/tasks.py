from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache

from query.models import BackFillStatus, Thread
from query.services.backfill_thread_service import BackFillThreadService
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
def classify_thread(thread_id: str) -> None:
    logger.info(f"classify_thread job started for the Thread {thread_id}")
    try:
        thread = Thread.objects.get(id=thread_id)
        ThreadClassificationService.classify(thread)
    except Thread.DoesNotExist:
        logger.error(f"Question Answer {thread_id} does not exist")


@shared_task
def back_fill_thread(thread_id: str) -> None:
    logger.info(f"back_fill_thread job started for the Thread {thread_id}")
    # Caching the thread to avoid the duplicate back filling
    with cache.lock(thread_id, timeout=600):
        thread = Thread.objects.get(id=thread_id)
        BackFillThreadService.back_fill_thread(thread)


@shared_task
def back_fill_threads_task() -> None:
    logger.info("back_fill_threads_task has job started")
    # extract 100 thread ids at a time that have not been backfilled
    thread_ids = BackFillStatus.objects.filter(is_back_filled=False).values_list(
        "id", flat=True
    )[:100]
    for thread_id in thread_ids:
        back_fill_thread.apply_async(kwargs={"thread_id": str(thread_id)})
