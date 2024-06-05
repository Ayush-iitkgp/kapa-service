from django.urls import path
from rest_framework.routers import DefaultRouter

from query.views.chat import ChatView
from query.views.threads import ThreadView, UpdateThreadLabelView

router = DefaultRouter()

urlpatterns = [
    path("v1/projects/<uuid:project_id>/chat", ChatView.as_view(), name="chat"),
    path(
        "v1/projects/<uuid:project_id>/threads/",
        ThreadView.as_view(
            {
                "get": "list",
            }
        ),
        name="threads-list",
    ),
    path(
        "v1/projects/<uuid:project_id>/update-label",
        UpdateThreadLabelView.as_view(),
        name="update-label",
    ),
]
