import logging

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from org.models import Project, ProjectAPIKey, Team, UserEmailSettings

logger = logging.getLogger(__name__)

User = get_user_model()


class ProjectAPIKeySerializer(serializers.ModelSerializer):
    private_api_key = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = ProjectAPIKey
        fields = "__all__"

    def create(self, validated_data):
        instance, private_key = ProjectAPIKey.objects.create_key(**validated_data)
        instance.private_api_key = private_key
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project model"""

    api_key = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = "__all__"
