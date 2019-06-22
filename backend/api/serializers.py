from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from authentication.models import User, Institute
from .models import *

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "city", "state")

class InstituteListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Institute
        fields = ("pk", "user", "pincode")

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class TestSeriesSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = TestSeries
        fields = ("id", "name", "price", "visible", "exam", "tests")

class UnitTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitTest
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'



