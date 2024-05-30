import pytest
from rest_framework.test import APIClient

from query.models import Thread

pytestmark = pytest.mark.django_db


@pytest.mark.asyncio
def test_get_threads_success_label_present(
    client_api_token: APIClient, thread: Thread
) -> None:
    project_id = thread.project.id
    response = client_api_token.get(f"/api/v1/{project_id}/threads/")
    assert response.status_code == 200
    result = response.data["results"][0]
    assert result["id"] == str(thread.id)
    assert result["project"] == project_id
    assert "label" in result
