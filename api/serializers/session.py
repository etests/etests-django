from django.template.loader import render_to_string
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import PermissionDenied

from api.models import Session, Test, Subject
from api.ses import send_email

from .test import TestSerializer


class SessionSerializer(ModelSerializer):
    test = SerializerMethodField()

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

    def get_test(self, obj):
        return TestSerializer(
            obj.test, context={"allow_answers": obj.practice or obj.test.status > 1}
        ).data

    def create(self, validated_data):
        test = Test.objects.get(id=validated_data.get("test_id"))
        sessions = Session.objects.filter(**validated_data)
        if sessions.filter(completed=False).count() > 0:
            return sessions.filter(completed=False)[0]
        elif test.status == 0:
            raise PermissionDenied("This test is not active yet.")
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
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if validated_data.get("completed", False):
            instance.evaluate(commit=False)
            test = instance.test
            send_email(
                instance.student.user.email,
                render_to_string(
                    "student_results/subject.txt", {"test_name": test.name}
                ),
                render_to_string(
                    "student_results/body.html",
                    {
                        "name": instance.student.user.name,
                        "test_name": test.name,
                        "date_time": instance.checkin_time,
                        "marks_obtained": instance.marks["total"],
                        "max_marks": instance.marks["max_marks"][-1],
                        "result_id": instance.id,
                    },
                ),
            )

        instance.save()

        return instance


class RanksSerializer(ModelSerializer):
    name = SerializerMethodField()
    subjects = SerializerMethodField()

    class Meta:
        model = Session
        fields = ("id", "name", "marks", "ranks", "practice", "subjects")

    def get_name(self, obj):
        return obj.student.user.name

    def get_subjects(self, obj):
        sections = obj.test.sections
        subjects = Subject.objects.all()
        return [subjects.get(id=section["subject"]).name for section in sections]

