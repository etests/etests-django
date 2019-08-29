from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from authentication.models import *
from .models import *
from authentication.serializers import UserDetailsSerializer, StudentDetailsSerializer, InstituteDetailsSerializer

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "city", "state")

class InstituteListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Institute
        fields = ("id", "user", "pincode")

class TestListSerializer(serializers.ModelSerializer):
    institute = InstituteListSerializer()

    class Meta:
        model=Test
        fields = ("id", "name", "active", "practice", "activation_time", "institute")

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields = ("name", "institute", "questions", "answers", "sections")

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields = '__all__'

class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id','name','institute','slug','active','practice','tags','date_added','activation_time','time_alotted','sections','questions')

class TestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id','name','institute','slug','active','practice','tags','date_added','activation_time','time_alotted')

class TestSeriesSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = TestSeries
        fields = ("id", "name", "price", "visible", "exam", "tests")

class SessionSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ('id', 'response', 'test', 'duration', 'current', 'completed')

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

class ResultSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ('id', 'test', 'marks')

class ReviewSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ('id', 'response', 'test', 'result', 'marks')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')

class CreditUseSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField('get_test_name')

    class Meta:
        model = CreditUse
        fields = ('__all__')

    def get_test_name(self, obj):
        return obj.test.name

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("pk", "institute", "batch", "roll_number", "joining_key")

class BatchJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("batch", "roll_number", "joining_key", "student")

class InstituteBatchSerializer(serializers.ModelSerializer):
    enrollments = BatchJoinSerializer(many=True)
    class Meta:
        model = Batch
        fields = ("pk", "name", "enrollments")

class BatchListSerializer(serializers.ModelSerializer):
    institute = InstituteDetailsSerializer()
    class Meta:
        model = Batch
        fields = ("pk", "name", "institute")
