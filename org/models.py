import logging
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from guardian.mixins import GuardianUserMixin
from rest_framework_api_key.models import AbstractAPIKey

from org.managers import UserManager
from query.src.enums import LabelEnum
from utils.models import AbstractBaseModel, AbstractProjectDependentModel

logger = logging.getLogger(__name__)


class User(AbstractBaseModel, AbstractUser, GuardianUserMixin):
    """
    Basic user model with email and name
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # kapa doesn't use usernames
    email = models.EmailField("email address", unique=True, db_index=True)
    is_email_verified = models.BooleanField(
        default=True
    )  # you can only log in via email OTP anyway
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, null=True, blank=True, related_name="users"
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


class UserEmailSettings(AbstractBaseModel):
    """User email settings model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    EMAIL_INTERVAL_CHOICES = [
        ("WEEKLY", "WEEKLY"),
        ("BIWEEKLY", "BIWEEKLY"),
        ("MONTHLY", "MONTHLY"),
    ]
    digest_email_interval = models.CharField(
        max_length=20, choices=EMAIL_INTERVAL_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.email}"


class Team(AbstractBaseModel):
    """
    Team model, this represents one of our customers, a company that
    is using kapa.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Project(AbstractBaseModel, AbstractProjectDependentModel):
    """
    This model represents an instance of the kapa.ai chatbot
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name="projects"
    )

    project_name = models.CharField(max_length=200)  # Airbyte
    product_name = models.CharField(max_length=100)  # for prompting: Airbyte
    labels = ArrayField(
        models.CharField(max_length=100),
        default=list([LabelEnum.DISCOVERY.title(), LabelEnum.TROUBLESHOOTING.title()]),
        blank=True,
        help_text="List of labels associated with the project",
    )

    def __str__(self):
        team_name = self.team.name if self.team else "No Team"
        return f"{team_name} - {self.project_name}"

    @property
    def parent_project(self):
        """
        We just need this method to be able to use the same permissions code
        for both the Project model and all other models that are dependent on
        a Project.
        """
        return self

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def update_labels(self, labels: list[str]) -> None:
        self.labels = labels
        self.save()


class ProjectAPIKey(AbstractAPIKey):
    """
    This API key is used to authenticate/authorize API calls.
    It needs to be sent in a `X-API-KEY` header.
    """

    projects = models.ManyToManyField(
        Project,
        related_name="api_keys",
        blank=True,
    )

    # Future: add a field for the type of API key, compatible
    # with the API key type field in the legacy API token model,
    # which will be deprecated eventually.

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Project API key"
        verbose_name_plural = "Project API keys"
