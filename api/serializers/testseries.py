from rest_framework.serializers import (
    ModelSerializer,
    ListSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from api.models import TestSeries, Payment

from .test import TestListSerializer


class TestSeriesSerializer(ModelSerializer):
    institute = StringRelatedField()
    exams = StringRelatedField(many=True)
    status = SerializerMethodField()

    class Meta:
        model = TestSeries
        fields = (
            "id",
            "name",
            "price",
            "visible",
            "exams",
            "tests",
            "institute",
            "status",
        )

    def get_status(self, obj):
        if not self.context["request"].user.is_authenticated:
            return 0
        elif not self.context["request"].user.is_student:
            return 1
        else:
            payments = Payment.objects.filter(
                student=self.context["request"].user.student, test_series=obj
            )
            if payments:
                return 4 if payments[0].verified else 3

            return 2


class TestSeriesDetialsSerializer(ModelSerializer):
    institute = StringRelatedField()
    tests = TestListSerializer(many=True, read_only=True)
    exams = StringRelatedField(many=True, read_only=True)
    status = SerializerMethodField()

    class Meta:
        model = TestSeries
        fields = (
            "id",
            "name",
            "price",
            "visible",
            "exams",
            "tests",
            "institute",
            "status",
        )

    def get_status(self, obj):
        if not self.context["request"].user.is_authenticated:
            return 0
        elif not self.context["request"].user.is_student:
            return 1
        else:
            payments = Payment.objects.filter(
                student=self.context["request"].user.student, test_series=obj
            )
            if payments:
                return 4 if payments[0].verified else 3

            return 2

