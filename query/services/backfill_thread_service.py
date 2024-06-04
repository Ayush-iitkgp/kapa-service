import logging

from django.db import transaction

from query.models import BackFillStatus, Thread
from query.services.thread_classification_service import ThreadClassificationService

logger = logging.getLogger(__name__)


class BackFillThreadService:
    @classmethod
    def back_fill_thread(cls, thread: Thread) -> None:
        # Make the backfill method to atomic
        with transaction.atomic():
            ThreadClassificationService.classify(thread)
            back_fill_status = BackFillStatus.objects.get(thread=thread)
            back_fill_status.update_status(is_back_filled=True)
