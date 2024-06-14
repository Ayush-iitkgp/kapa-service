import pytest
from rest_framework.test import APIClient

from org.models import Project
from query.models import Thread

pytestmark = pytest.mark.django_db


def test_update_thread_label(
    client_api_token: APIClient, thread: Thread, project: Project
) -> None:
    project_id = thread.project.id
    labels = list(project.labels)
    thread.update_label(labels[0])
    new_label = labels[1]
    thread.refresh_from_db()
    assert thread.label != new_label
    response = client_api_token.patch(
        f"/query/v1/projects/{project_id}/threads/",
        data={
            "thread_id": str(thread.id),
            "new_label": new_label,
            "comment": "label updated by ayush",
            "user_id": "e003e31e-54e5-41cd-8e8f-5af16c231085",
        },
    )
    assert response.status_code == 200
    result = response.data
    assert result["id"] == str(thread.id)
    assert result["project"] == project_id
    assert result["label"] == new_label
    thread.refresh_from_db()
    assert thread.label == new_label
