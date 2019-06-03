from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ("id", "name", "email", "phone", "state", "city", "password", "is_student", "is_institute")

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.state = validated_data.get('state', instance.state)
        instance.city = validated_data.get('city', instance.city)
        if validated_data.get('password', None):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
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


class InstituteSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Institute
        extra_kwargs = {'pk': {'read_only': True}}
        fields = ("pk", "user", "pincode")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        institute, created = Institute.objects.update_or_create(
            user=user, pincode=validated_data.pop("pincode")
        )
        return institute
