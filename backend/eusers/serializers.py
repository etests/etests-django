from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "state", "city")


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ("user", "gender", "institute", "birth_date")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student, created = Student.objects.update_or_create(
            user=user,
            gender=validated_data.pop("gender"),
            institute=validated_data.pop("institute"),
            birth_date=validated_data.pop("birth_date"),
        )
        return student


class InstituteSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Institute
        fields = ("user", "pincode")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        institute, created = Institute.objects.update_or_create(
            user=user, gender=validated_data.pop("pincode")
        )
        return institute
