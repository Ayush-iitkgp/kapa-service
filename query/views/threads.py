import logging
import uuid
from typing import Union

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from org.models import Project
from org.permissions import HasProjectAPIKey
from query.models import LabelReview, Thread
from query.serializers import ThreadSerializer, UpdateThreadLabelInputSerializer

logger = logging.getLogger(__name__)


class ThreadView(viewsets.ModelViewSet):
    """
    View for the 'Thread' model
    """

    serializer_class = ThreadSerializer
    permission_classes = [HasProjectAPIKey]
    http_method_names = ["get"]

    def get_queryset(self) -> models.QuerySet:
        project_id = self.kwargs.get("project_id")
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            return Thread.objects.filter(project=project)
        raise ValidationError("Project ID is required")


class UpdateThreadLabelView(APIView):
    permission_classes = [HasProjectAPIKey]
    serializer_class = ThreadSerializer

    def patch(self, request: Request, project_id: Union[uuid.UUID, str]):
        project = get_object_or_404(Project, id=project_id)
        logger.info(f"Updating label for thread {project.id}")
        serializer = UpdateThreadLabelInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        thread_id = validated_data.get("thread_id")
        thread = get_object_or_404(Thread, id=thread_id)
        new_label = validated_data.get("new_label")
        if new_label not in project.labels:
            return Response(
                data={"error": f"allowed label are {list(project.labels)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # TODO: Do we need to make creating a new record and updating the thread atomic?
        _ = LabelReview.objects.create(
            thread=thread,
            user_id=validated_data.get("user_id"),
            comment=validated_data.get("comment"),
            old_label=thread.label,
            new_label=validated_data.get("new_label"),
        )
        thread.update_label(new_label)
        logger.info(
            f"Updated label for thread {project.id} with new label as {new_label}"
        )
        thread_serializer = self.serializer_class(thread)
        return Response(thread_serializer.data, status=status.HTTP_200_OK)
