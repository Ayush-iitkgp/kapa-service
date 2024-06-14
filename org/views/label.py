import logging
import uuid
from typing import Union

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from org.models import Project
from org.permissions import HasProjectAPIKey
from org.serializers import LabelInputSerializer, ProjectSerializer

logger = logging.getLogger(__name__)


class ProjectLabelView(APIView):
    permission_classes = [HasProjectAPIKey]
    serializer_class = ProjectSerializer

    def post(self, request: Request, project_id: Union[uuid.UUID, str]) -> Response:
        project, labels = self.validate_request(request, project_id)
        logger.info(project.labels)
        existing_labels = project.labels
        if existing_labels is not None and len(existing_labels) > 0:
            # TODO: Is 400 a correct status code to send?
            return Response(
                {
                    "error": "Create labels not allowed for the the project for which it already exist"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        project.update_labels(labels)
        logger.info(f"Project {project.id} labels created")
        project_serializer = self.serializer_class(project)
        return Response(project_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, project_id) -> Response:
        project, labels = self.validate_request(request, project_id)
        project.update_labels(labels)
        logger.info(f"Project {project.id} labels updated")
        project_serializer = self.serializer_class(project)
        return Response(project_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id) -> Response:
        project = get_object_or_404(Project, id=project_id)
        project.update_labels([])
        logger.info(f"Project {project.id} labels deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def validate_request(
        request: Request, project_id: Union[uuid.UUID, str]
    ) -> (Project, list[str]):
        project = get_object_or_404(Project, id=project_id)
        serializer = LabelInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        labels = serializer.validated_data.get("labels")
        return project, labels
