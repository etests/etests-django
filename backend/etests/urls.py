from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="eTests API")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", schema_view, name="swagger_schema"),
    path("rest/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("authentication.urls")),
    path("", include("api.urls"))
]
