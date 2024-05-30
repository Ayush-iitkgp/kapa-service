import uuid

from django.core.exceptions import ValidationError
from django.db import models

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
    label = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return f"Thread for {self.project} {self.id}"

    @property
    def parent_project(self):
        return self.project

    def clean(self):
        super().clean()
        if self.label is not None and self.label not in self.project.labels:
            raise ValidationError(
                f"The label '{self.label}' is not in the project's defined labels."
            )

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


class LabelReview(AbstractBaseModel, AbstractProjectDependentModel):
    """
    A model representing a LabelReview, which has a 1:1 relationship with Thread.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.OneToOneField(
        Thread, on_delete=models.CASCADE, related_name="review"
    )
    user_id = models.UUIDField(null=True, default=None, editable=False)
    comment = models.TextField()
    old_label = models.CharField(max_length=100, default=None)
    new_label = models.CharField(max_length=100, default=None)

    def __str__(self):
        return f"Label review for {self.thread} {self.id}"

    @property
    def parent_project(self):
        return self.thread.project

    # TODO: Also, add the restriction on the old and the new label that it should be one of the possible values
    #  as allowed by the project

    class Meta:
        verbose_name = "Label Review"
        verbose_name_plural = "Label Reviews"
