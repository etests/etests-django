from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from api.models import Batch


class BatchListSerializer(ModelSerializer):
    class Meta:
        model = Batch
        fields = ("id", "name", "institute")


class BatchJoinSerializer(Serializer):
    roll_number = CharField()
    joining_key = CharField()

    def validate(self, attrs):
        try:
            enrollment = self.instance.enrollments.get(
                roll_number=attrs["roll_number"], joining_key=attrs["joining_key"]
            )
        except Enrollment.DoesNotExist:
            raise ValidationError("Invalid roll number or joining key")

        if enrollment.student is not None:
            raise ValidationError("This joining key has been already used")
        else:
            self.enrollment = enrollment

        return attrs

    def save(self):
        self.enrollment.student = self.context.get("request").user.student
        self.enrollment.date_joined = datetime.now()
        self.enrollment.save()
