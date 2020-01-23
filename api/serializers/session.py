from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import PermissionDenied

from api.models import Session, Test

from .test import TestSerializer

class SessionListSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "practice", "checkin_time", "completed")


class SessionSerializer(ModelSerializer):
    test = TestSerializer(read_only=True)

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
            "ranks",
            "result",
            "marks",
        )

        read_only_fields = (
            "id",
            "practice",
            "checkin_time",
            "duration",
            "ranks",
            "result",
            "marks",
        )

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

    def update(self, instance, validated_data):
        if validated_data.get("completed", False):
            instance.evaluate(commit=False)

        instance.save()

        return instance


class RanksSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Session
        fields = ("id", "name", "marks", "ranks", "practice")

    def get_name(self, obj):
        return obj.student.user.name
