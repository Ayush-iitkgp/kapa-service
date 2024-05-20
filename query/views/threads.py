from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from org.models import Project
from org.permissions import HasProjectAPIKey
from query.models import Thread
from query.serializers import ThreadSerializer


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
