import pytest
from rest_framework import status
from rest_framework.test import APIClient

from org.models import Project

pytestmark = pytest.mark.django_db


def test_post_project_labels_success(
    client_api_token: APIClient, project: Project
) -> None:
    project_id = project.id
    project.update_labels([])
    project.refresh_from_db()
    response = client_api_token.post(
        f"/org/v1/projects/{project_id}/labels",
        data={"labels": ["first label", "second label"]},
    )
    assert response.status_code == status.HTTP_201_CREATED
    project.refresh_from_db()
    assert project.labels == ["first label", "second label"]


def test_patch_project_labels_success(
    client_api_token: APIClient, project: Project
) -> None:
    project_id = project.id
    response = client_api_token.patch(
        f"/org/v1/projects/{project_id}/labels",
        data={"labels": ["first label", "second label", "new label"]},
    )
    assert response.status_code == status.HTTP_200_OK
    project.refresh_from_db()
    assert project.labels == ["first label", "second label", "new label"]


def test_delete_project_labels_success(
    client_api_token: APIClient, project: Project
) -> None:
    project_id = project.id
    response = client_api_token.delete(f"/org/v1/projects/{project_id}/labels")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    project.refresh_from_db()
    assert project.labels == []
