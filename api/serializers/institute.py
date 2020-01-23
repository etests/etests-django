from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Enrollment, Institute

from .batch import BatchSerializer
from .user import UserSerializer


class InstituteListSerializer(ModelSerializer):
    batches = BatchSerializer(many=True, read_only=True)
    user = UserSerializer()

    class Meta:
        model = Institute
        fields = ("id", "user", "pincode", "test_series", "batches", "rating", "about")


class JoinedInstitutesSerializer(ModelSerializer):
    batches = BatchSerializer(many=True, read_only=True)
    user = UserSerializer()
    enrollments = SerializerMethodField()

    class Meta:
        model = Institute
        fields = ("id", "user", "batches", "enrollments")

    def get_enrollments(self, obj):
        return [
            enrollment.batch.id
            for enrollment in Enrollment.objects.filter(
                student=self.context["request"].user.student, institute=obj
            )
            if enrollment.batch
        ]
