from rest_framework.serializers import ModelSerializer, StringRelatedField, CharField

from api.models import Institute


class StudentSerializer(ModelSerializer):
    joining_key = CharField()
    students = StringRelatedField(many=True)

    class Meta:
        model = Institute
        fields = ("id", "joining_key", "students")
