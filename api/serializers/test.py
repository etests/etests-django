from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Test


class TestInfoSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "status",
            "date_added",
            "activation_time",
            "closing_time",
            "time_alotted",
        )


class StudentTestListSerializer(ModelSerializer):
    institute = SerializerMethodField()
    sessions = SerializerMethodField()

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
            "sessions",
            "free",
            "syllabus",
        )

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

    def get_sessions(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated and user.is_student:
            serializer_context = {"request": self.context.get("request")}
            sessions = Session.objects.filter(test=obj, student=user.student)
            return SessionListSerializer(
                sessions, many=True, read_only=True, context=serializer_context
            ).data
        else:
            return None


class TestListSerializer(ModelSerializer):
    institute = SerializerMethodField()
    exam = SerializerMethodField()

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

    def get_exam(self, obj):
        if obj.exam is not None:
            return obj.exam.name
        else:
            return ""

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
        exclude = ("registered_students", "marks_list")


class StudentTestSerializer(ModelSerializer):
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
            "free",
            "syllabus",
        )
