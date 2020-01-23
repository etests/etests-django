from rest_framework.serializers import ModelSerializer
from api.models import Enrollment


class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Enrollment
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

