from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    StringRelatedField,
    CharField,
    PrimaryKeyRelatedField,
)

from api.models import Institute, User


class StudentSerializer(ModelSerializer):
    # Student id is required to make delete requests on institute students
    id = PrimaryKeyRelatedField(source="student", read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "image")

    def update(self, instance, validated_data):
        instance.students.remove(validated_data.get("id"))
        return instance


class JoiningKeySerializer(Serializer):
    joining_key = CharField()

    class Meta:
        fields = ("joining_key",)

    def update(self, instance, validated_data):
        instance.joining_key = validated_data.get("joining_key")
        instance.save()
        return instance
