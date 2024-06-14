from django.urls import path
from rest_framework.routers import DefaultRouter

from query.views.chat import ChatView
from query.views.threads import ThreadView

router = DefaultRouter()

urlpatterns = [
    path("v1/projects/<uuid:project_id>/chat", ChatView.as_view(), name="chat"),
    path(
        "v1/projects/<uuid:project_id>/threads/",
        ThreadView.as_view(
            {
                "get": "list",
                "patch": "patch",
            }
        ),
        name="threads-list",
    ),
]
