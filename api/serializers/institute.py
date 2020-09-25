from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    SlugRelatedField,
    CharField,
)

from api.models import Institute, Contact, Batch

from .user import UserSerializer
from rest_framework.exceptions import ValidationError


class InstituteListSerializer(ModelSerializer):
    image = SerializerMethodField()

    class Meta:
        model = Institute
        fields = ("id", "name", "pincode", "test_series", "rating", "about", "image")

    def get_image(self, obj):
        return obj.user.image


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
            "questions",
            "gallery",
            "faqs",
            "courses",
            "centers",
            "contacts",
            "faculty",
            "links",
            "forms",
            "extras",
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
