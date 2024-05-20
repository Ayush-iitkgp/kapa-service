from celery import shared_task

from query.src.email_report import EmailReportGenerator


@shared_task
def send_weekly_email_report() -> None:
    """
    Sends periodic email report.
    """
    generator = EmailReportGenerator()
    generator.send_reports()
