"""
URL configuration for kapa_ingestion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import re

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

SCHEMA_TITLE = "Kapa.ai"
SCHEMA_DESCRIPTION = "API for Kapa.ai"
SCHEMA_VERSION = "1.0.0"
SCHEMA_DEFAULT_VERSION = "v1"
SCHEMA_TERMS_OF_SERVICE = "https://www.kapa.ai/terms"


openapi_schema_private = get_schema_view(
    openapi.Info(
        title=SCHEMA_TITLE,
        description=SCHEMA_DESCRIPTION,
        version=SCHEMA_VERSION,
        default_version=SCHEMA_DEFAULT_VERSION,
        terms_of_service=SCHEMA_TERMS_OF_SERVICE,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("query/", include("query.urls")),
    path("org/", include("org.urls")),
    path("drf/", include("rest_framework.urls")),
    path(
        "redoc",
        openapi_schema_private.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-private",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
