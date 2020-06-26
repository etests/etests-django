from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    StringRelatedField,
    CharField,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from api.models import Institute, User


class StudentSerializer(ModelSerializer):
    # Student id is required to make delete requests on institute students
    id = PrimaryKeyRelatedField(source="student", read_only=True)
    batch = SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "image", "batch")

    def update(self, instance, validated_data):
        instance.students.remove(validated_data.get("id"))
        return instance

    def get_batch(self, obj):
        if obj.is_student and obj.student.batch:
            return obj.student.batch.name


class JoiningKeySerializer(Serializer):
    joining_key = CharField()

    class Meta:
        fields = ("joining_key",)

    def update(self, instance, validated_data):
        instance.joining_key = validated_data.get("joining_key")
        instance.save()
        return instance
