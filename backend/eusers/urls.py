from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"students", StudentViewSet)
router.register(r"institutes", InstituteViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
