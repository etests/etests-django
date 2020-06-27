from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
    StringRelatedField,
    SerializerMethodField,
    PrimaryKeyRelatedField,
)
from api.models import Enrollment, Batch, Institute, User
from api.serializers.bulk import BulkSerializerMixin, BulkListSerializer


class StudentEnrollmentListSerializer(ModelSerializer):
    institute = StringRelatedField()
    batch_name = StringRelatedField(source="batch")

    class Meta:
        model = Enrollment
        fields = ("id", "institute", "batch", "batch_name", "roll_number")


class StudentEnrollmentSerializer(ModelSerializer):
    joining_key = CharField()
    batch_name = StringRelatedField(source="batch")

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "institute",
            "batch",
            "batch_name",
            "roll_number",
            "student",
            "joining_key",
        )
        extra_kwargs = {"institute": {"required": False}}

    def validate(self, attrs):
        batch = attrs.get("batch", None)

        enrollments = Enrollment.objects.filter(
            batch=batch, student=self.context.get("request").user.student
        )
        if len(enrollments):
            raise ValidationError("You already joined this batch.")

        if batch.joining_key != attrs.get("joining_key", None):
            raise ValidationError("Invalid joining key")

        return attrs

    def create(self, validated_data):
        validated_data.pop("joining_key", None)
        institute = validated_data.get("batch").institute
        enrollment = Enrollment.objects.create(institute=institute, **validated_data)

        return enrollment


class StudentUserSerializer(ModelSerializer):
    # Student id is required to make delete requests on institute students
    id = PrimaryKeyRelatedField(source="student", read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "image")


class EnrollmentSerializer(ModelSerializer):
    student = SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ("id", "institute", "batch", "roll_number", "student", "date_joined")
        read_only_fields = ("student", "date_joined")
        extra_kwargs = {"institute": {"required": False}}

    def get_student(self, obj):
        return StudentUserSerializer(instance=obj.student.user).data
