from django.db import models
from django.utils import timezone


class AbstractBaseModel(models.Model):
    """
    Abstract base model to be inherited by all models
    that need to have created_at and updated_at fields.
    """

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractProjectDependentModel(models.Model):
    """
    An abstract model representing a model that is dependent on a Project.

    It is used to add a parent_project property to the model, which is used
    in the permissions code to check if the user has access to the project
    that the model is associated with.
    """

    class Meta:
        abstract = True

    @property
    def parent_project(self):
        raise NotImplementedError
