import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_api_key.models import AbstractAPIKey

from org.models import Project
from utils.models import AbstractBaseModel, AbstractProjectDependentModel


class Thread(AbstractBaseModel, AbstractProjectDependentModel):
    """
    A model representing a Thread, which has a 1:N relationship with QuestionAnswer.

    Threads represent conversations between a user and kapa.ai.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="threads"
    )

    def __str__(self):
        return f"Thread for {self.project} {self.id}"

    @property
    def parent_project(self):
        return self.project

    class Meta:
        verbose_name = "Thread"
        verbose_name_plural = "Threads"


class QuestionAnswer(AbstractBaseModel, AbstractProjectDependentModel):
    """
    A model representing a QuestionAnswer, which has a 1:N relationship with Thread.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="question_answers"
    )

    question = models.TextField()  # the question that was sent to kapa.ai
    answer = models.TextField()  # the answer kapa.ai generated

    def __str__(self):
        return self.question

    @property
    def parent_project(self):
        return self.thread.project

    class Meta:
        verbose_name = "Question/Answer Item"
        verbose_name_plural = "Question/Answer Items"
