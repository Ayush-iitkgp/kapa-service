from django.urls import include, path
from rest_framework.routers import DefaultRouter

from org.views.label import ProjectLabelView

router = DefaultRouter()

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/projects/<uuid:project_id>/labels", ProjectLabelView.as_view(), name="label"
    ),
]
