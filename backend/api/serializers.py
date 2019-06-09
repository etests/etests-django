from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from authentication.models import User, Institute

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "city", "state")

class InstituteListSerializr(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Institute
        fields = ("pk", "user", "pincode")