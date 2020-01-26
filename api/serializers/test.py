from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from api.models import Session, Test


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
            "syllabus",
            "sessions",
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
        )
        extra_kwargs = {
            "test_series": {"required": False},
            "status": {"read_only": True},
        }


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
            "tags",
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
