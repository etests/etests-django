from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from api.models import Institute

from .user import UserSerializer


class InstituteListSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Institute
        fields = ("id", "user", "pincode", "test_series", "rating", "about")


class JoinedInstitutesSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Institute
        fields = ("id", "user")
