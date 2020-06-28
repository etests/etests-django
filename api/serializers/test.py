from time import sleep
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    Serializer,
    BooleanField,
)

from api.models import Session, Test, TestSeries


class SessionListSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "practice", "checkin_time", "completed")


class TestListSerializer(ModelSerializer):
    institute = SerializerMethodField()
    exam = StringRelatedField()
    sessions = SerializerMethodField()

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "status",
            "aits",
            "activation_time",
            "closing_time",
            "time_alotted",
            "institute",
            "exam",
            "free",
            "status",
            "syllabus",
            "sessions",
            "registered_batches",
        )

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

    def get_sessions(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated and user.is_student:
            sessions = Session.objects.filter(test=obj, student=user.student)
            return SessionListSerializer(sessions, many=True, read_only=True).data


class TestCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "aits",
            "activation_time",
            "closing_time",
            "time_alotted",
            "institute",
            "questions",
            "answers",
            "sections",
            "test_series",
            "exam",
            "status",
            "free",
            "syllabus",
            "registered_batches",  # FIXME: Should be shown to owner institute only
        )
        extra_kwargs = {
            "test_series": {"required": False},
            "status": {"read_only": True},
        }

    def create(self, validated_data):
        exam = validated_data.get("exam", None)
        test_series = validated_data.get("test_series", [])

        if test_series and exam:
            for ts in test_series:
                ts.exams.add(exam)

        return super().create(validated_data)


class TestSerializer(ModelSerializer):
    answers = SerializerMethodField()

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "institute",
            "status",
            "aits",
            "date_added",
            "activation_time",
            "closing_time",
            "time_alotted",
            "sections",
            "questions",
            "answers",
            "free",
            "syllabus",
        )

    def get_answers(self, obj):
        if self.context.get("allow_answers", False):
            return obj.answers


class TestEvaluationSerializer(Serializer):
    include_practice = BooleanField(default=False)
    include_evaluated = BooleanField(default=False)
    generate_ranks = BooleanField(default=False)

    class Meta:
        fields = ("include_practice", "include_evaluated", "generate_ranks")

    def save(self):
        generate_ranks = self.validated_data.pop("generate_ranks")
        self.instance.evaluate_sessions(**self.validated_data)
        if generate_ranks:
            sleep(2)
            self.instance.generate_ranks()
        return self.instance
