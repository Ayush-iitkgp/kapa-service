import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from org.models import UserEmailSettings

logger = logging.getLogger(__name__)


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_email_settings(sender, instance, created, **kwargs):
    """
    Create a UserEmailSettings object when a new user is created.
    """
    if created:
        UserEmailSettings.objects.create(user=instance)
