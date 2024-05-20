import logging
from datetime import timedelta

from django.utils.timezone import now

from org.models import Project
from query.models import QuestionAnswer

logger = logging.getLogger(__name__)


class EmailReportGenerator:
    def send_reports(self) -> None:
        """
        In the real system this function would compute a weekly email report with usage statistics
        and send to our customers.

        For simplicity of this excercise it just logs the total count of messages from the last week
        for each project.
        """

        one_week_ago = now() - timedelta(days=7)

        projects = Project.objects.all()
        for project in projects:
            last_week_count = QuestionAnswer.objects.filter(
                thread__project=project, created_at__gte=one_week_ago
            ).count()
            logger.info(
                f"Project: {project.project_name} - Messages in the last week: {last_week_count}"
            )
