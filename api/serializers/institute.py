from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    SlugRelatedField,
    CharField,
)

from api.models import Institute, Contact

from .user import UserSerializer
from rest_framework.exceptions import ValidationError


class InstituteListSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = ("id", "name", "pincode", "test_series", "rating", "about")


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
            "forms"
        )


class JoinInstituteSerializer(Serializer):
    joining_key = CharField()

    def validate(self, attrs):
        if self.instance.joining_key != attrs.get("joining_key", None):
            raise ValidationError("Invalid joining key")
        return attrs

    def save(self, student):
        if self.instance.joining_key == self.validated_data.get("joining_key", None):
            self.instance.students.add(student)


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
