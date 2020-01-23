from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import Institute


class InstituteListSerializer(ModelSerializer):
    batches = BatchListSerializer(many=True, read_only=True)
    user = UserSerializer()
    test_series = SerializerMethodField()

    class Meta:
        model = Institute
        fields = ("id", "user", "pincode", "test_series", "batches", "rating", "about")

    def get_test_series(self, obj):
        serializer_context = {"request": self.context.get("request")}
        test_series = obj.test_series.filter(institute__verified=True, visible=True)
        serializer = TestSeriesSerializer(
            test_series, many=True, context=serializer_context
        )
        return serializer.data


class InstituteBatchSerializer(ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, required=False)

    class Meta:
        model = Batch
        fields = ("id", "name", "enrollments")


class JoinedInstitutesSerializer(ModelSerializer):
    batches = BatchListSerializer(many=True, read_only=True)
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
