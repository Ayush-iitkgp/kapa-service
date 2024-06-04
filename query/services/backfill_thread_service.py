import logging

from query.models import Thread

logger = logging.getLogger(__name__)


class BackfillThreadService:
    @classmethod
    def backfill_thread(cls, thread: Thread) -> None:
        pass
