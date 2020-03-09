from rest_framework.serializers import ModelSerializer
from api.models import Enrollment
from api.serializers.bulk import BulkSerializerMixin, BulkListSerializer


class EnrollmentSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = Enrollment
        list_serializer_class = BulkListSerializer
        fields = (
            "id",
            "institute",
            "batch",
            "roll_number",
            "joining_key",
            "student",
            "date_joined",
        )
        read_only_fields = ("student", "date_joined")
        extra_kwargs = {"institute": {"required": False}}

