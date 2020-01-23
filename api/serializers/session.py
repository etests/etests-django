from rest_framework import serializers

from api.models import Session, Test


class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "practice", "checkin_time", "completed")


class SessionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    test = StudentTestSerializer(read_only=True)
    completed = serializers.BooleanField(default=False)
    practice = serializers.BooleanField(read_only=True)
    checkin_time = serializers.DateTimeField(read_only=True)
    duration = serializers.DurationField(read_only=True)
    current = serializers.JSONField(required=False)
    response = serializers.JSONField(required=False)

    class Meta:
        model = Session
        fields = (
            "id",
            "test",
            "completed",
            "practice",
            "checkin_time",
            "duration",
            "current",
            "response",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get("request").method == "POST":
            self.fields.get("response").read_only = True
            self.fields.get("current").read_only = True
            self.fields.get("completed").read_only = True

    def create(self, validated_data):
        test = Test.objects.get(id=validated_data.get("test_id"))
        sessions = Session.objects.filter(**validated_data)
        if sessions.filter(completed=False).count() > 0:
            return sessions.filter(completed=False)[0]
        elif (
            test.status == 1
            and sessions.filter(completed=True, practice=False).count() > 0
        ):
            raise PermissionDenied(
                "You have already attempted the test. You can practice after the live test ends."
            )
        else:
            return super().create(validated_data)


class PracticeSessionSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = (
            "id",
            "practice",
            "response",
            "test",
            "checkin_time",
            "duration",
            "current",
            "completed",
            "result",
            "marks",
            "ranks",
        )
        extra_kwargs = {"ranks": {"read_only": True}}


class ResultSerializer(serializers.ModelSerializer):
    test = StudentTestSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = ("id", "response", "test", "marks", "completed")


class ReviewSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = ("id", "response", "test", "result", "marks", "completed", "ranks")


class RankListSerializer(serializers.ModelSerializer):
    roll_number = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ("id", "roll_number", "name", "marks", "ranks", "practice")

    def get_roll_number(self, obj):
        try:
            return Enrollment.objects.get(
                student=obj.student, institute=obj.test.institute
            ).roll_number
        except:
            return "-"

    def get_name(self, obj):
        return obj.student.user.name
