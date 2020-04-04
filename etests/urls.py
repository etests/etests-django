from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="eTests API",
        default_version="v1",
        description="Test description",
        contact=openapi.Contact(email="etests.service@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
admin.site.site_header = "eTests API Administration"
admin.site.site_title = "eTests API"
admin.site.index_title = "Administration Panel"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("rest/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("api.urls")),
    path("oauth/", include("rest_framework_social_oauth2.urls")),
]
