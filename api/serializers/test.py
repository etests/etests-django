from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from api.models import Test


class TestListSerializer(ModelSerializer):
    institute = SerializerMethodField()
    exam = StringRelatedField()

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
        )

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}


class TestCreateSerializer(ModelSerializer):
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
