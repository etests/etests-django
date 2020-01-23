from rest_framework.serializers import (
    ModelSerializer,
    ListSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from api.models import TestSeries, Payment

from .test import TestListSerializer


class FilteredListSerializer(ListSerializer):
    def to_representation(self, data):
        if (
            not self.context["request"].user.is_authenticated
            or self.context["request"].user.is_student
        ):
            data = data.filter(institute__verified=True, visible=True)
        elif self.context["request"].user.is_staff:
            pass
        elif self.context["request"].user.is_institute:
            data = data.filter(institute=self.context["request"].user.institute)

        return super(FilteredListSerializer, self).to_representation(data)


class TestSeriesSerializer(ModelSerializer):
    tests = TestListSerializer(many=True, read_only=True)
    institute = SerializerMethodField()
    exams = StringRelatedField(many=True)
    status = SerializerMethodField()

    class Meta:
        list_serializer_class = FilteredListSerializer
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
                user=self.context["request"].user, test_series=obj
            )
            if payments:
                return 4 if payments[0].verified else 3
            
            return 2

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

