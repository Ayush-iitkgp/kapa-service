import logging

from django.conf import settings
from rest_framework_api_key.permissions import BaseHasAPIKey

from org.models import ProjectAPIKey, Team, User

logger = logging.getLogger(__name__)


class HasProjectAPIKey(BaseHasAPIKey):
    model = ProjectAPIKey
    """
    Permission that allows access to the resource if the request has a valid API key
    that is associated with the given project.
    """
    HTTP_HEADER = getattr(settings, "API_KEY_CUSTOM_HEADER", "HTTP_AUTHORIZATION")

    def get_api_key(self, request):
        key = request.META.get(self.HTTP_HEADER)
        if not key:
            return None
        # This is to ensure that DRF raises a 403 instead of a 401
        # request._authenticator = api_key
        request._authenticator = key
        try:
            return ProjectAPIKey.objects.get_from_key(key)
        except ProjectAPIKey.DoesNotExist:
            return None

    def has_permission(self, request, view) -> bool:
        api_key = self.get_api_key(request)
        if not api_key:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        api_key = self.get_api_key(request)
        if not api_key:
            return False

        if isinstance(obj, ProjectAPIKey):
            return obj == api_key
        elif isinstance(obj, (Team, User)):
            return self.has_user_or_team_permission(api_key, obj)
        else:
            return self.has_generic_object_permission(api_key, obj)

    def has_user_or_team_permission(self, api_key, obj):
        """
        Special cases: Object is "Team"/"User" instance:
        We need to check if the instance is associated with the API Key.
        Given that API keys are associated with projects, the checks
        for team and user instances are different.
        """
        projects = api_key.projects.values_list("id", flat=True)
        if isinstance(obj, Team):
            teams = Team.objects.filter(project__id__in=projects)
            return obj in teams
        if isinstance(obj, User):
            teams = Team.objects.filter(project__id__in=projects)
            return obj.team in teams

    def has_generic_object_permission(self, api_key, obj):
        if not hasattr(obj, "parent_project"):
            logger.error(
                "Object does not have parent_project attribute. Cannot check ownership."
            )
            return False
        return obj.parent_project.id in api_key.projects.values_list("id", flat=True)
