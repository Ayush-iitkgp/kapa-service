import pytest
from django.core.exceptions import ValidationError

from query.models import Project, Thread

pytestmark = pytest.mark.django_db


def test_label_not_present_throws_validation_error(project: Project):
    thread = Thread.objects.create(project=project)
    with pytest.raises(ValidationError):
        thread.label = "some random_label"
        thread.save()
