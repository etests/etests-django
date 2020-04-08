from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    SlugRelatedField,
)

from api.models import Institute, Contact

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
            "settings",
            "carousel",
            "notifications",
            "features",
            "team",
            "toppers",
            "downloads",
            "gallery",
            "faqs",
            "courses",
        )


class JoinedInstitutesSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Institute
        fields = ("id", "user")


class ContactSerializer(ModelSerializer):
    institute = SlugRelatedField(
        slug_field="handle", queryset=Institute.objects.filter(verified=True)
    )

    class Meta:
        model = Contact
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "description",
            "institute",
        )
