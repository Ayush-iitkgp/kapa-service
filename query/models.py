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
    label_id = models.UUIDField(null=True, default=None, editable=False)

    def __str__(self):
        return f"Thread for {self.project} {self.id}"

    @property
    def parent_project(self):
        return self.project

    def clean(self):
        super().clean()
        if self.label_id:
            if not Label.objects.filter(
                id=self.label_id, project=self.project
            ).exists():
                raise ValidationError(
                    "label_id must be a UUID of a label associated with the same project."
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


class Label(AbstractBaseModel, AbstractProjectDependentModel):
    """
    A model representing a Label, which has a 1:N relationship with Project.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="labels"
    )
    name = models.TextField()  # the name of the label for the conversation

    def __str__(self):
        return self.name

    @property
    def parent_project(self):
        return self.project

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = "Labels"


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
    old_category_id = models.UUIDField(null=True, default=None, editable=False)
    new_category_id = models.UUIDField(null=True, default=None, editable=False)

    def __str__(self):
        return f"Label review for {self.thread} {self.id}"

    @property
    def parent_project(self):
        return self.thread.project

    class Meta:
        verbose_name = "Label Review"
        verbose_name_plural = "Label Reviews"
