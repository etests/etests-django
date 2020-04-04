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


class InstituteDetailsSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Institute
        fields = (
            "id",
            "handle",
            "user",
            "pincode",
            "test_series",
            "rating",
            "about",
            "carousel",
            "features",
            "team",
            "toppers",
            "downloads",
            "gallery",
            "faqs",
        )


class JoinedInstitutesSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Institute
        fields = ("id", "user")
