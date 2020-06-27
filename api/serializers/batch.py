from datetime import datetime

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
)

from api.models import Batch, Enrollment

from .enrollment import EnrollmentSerializer


class BatchSerializer(ModelSerializer):
    institute_name = StringRelatedField(source="institute")

    class Meta:
        model = Batch
        fields = ("id", "name", "institute", "institute_name")


class BatchEnrollmentsSerializer(ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, required=False)

    class Meta:
        model = Batch
        fields = ("id", "name", "enrollments", "joining_key")
