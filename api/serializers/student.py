from rest_framework.serializers import ModelSerializer, StringRelatedField

from api.models import Student


class StudentSerializer(ModelSerializer):
    name = StringRelatedField(read_only=True, source="user")

    class Meta:
        model = Student
        fields = ("id", "name")
