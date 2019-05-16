from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token, refresh_jwt_token
from .serializers import TokenSerializer

schema_view = get_swagger_view(title="eTests API")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", schema_view, name="swagger_schema"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("eusers.urls")),
    path("auth/obtain_token/", ObtainJSONWebToken.as_view(serializer_class=TokenSerializer)),
    path("auth/refresh_token/", refresh_jwt_token),
]
