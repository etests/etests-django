from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from authentication.models import *
from .models import *
from authentication.serializers import UserDetailsSerializer, StudentDetailsSerializer, InstituteDetailsSerializer

class TestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id','name', 'status', 'date_added', 'activation_time', 'time_alotted')

class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'practice', 'checkin_time', 'completed')

class StudentTestListSerializer(serializers.ModelSerializer):
    institute = serializers.SerializerMethodField()
    sessions = SessionListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ('id','name','institute', 'status', 'practice', 'date_added', 'activation_time', 'time_alotted', "sessions")
    
    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(institute__verified = True, visible = True)
        return super(FilteredListSerializer, self).to_representation(data)

class TestSeriesSerializer(serializers.ModelSerializer):
    tests = StudentTestListSerializer(many=True, read_only=True)
    institute = serializers.SerializerMethodField()
    exams = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = TestSeries
        fields = ("id", "name", "price", "visible", "exams", "tests", "institute")

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

    def get_exams(self, obj):
        return [exam.name for exam in obj.exams.all()]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "city", "state")

class InstituteListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    test_series = TestSeriesSerializer(many=True)

    class Meta:
        model = Institute
        fields = ("id", "user", "pincode", "test_series")

class ExamListSerializer(serializers.ModelSerializer):
    test_series = TestSeriesSerializer(many=True)

    class Meta:
        model = Exam
        fields = ("id", "name", "start_date", "test_series", "image")

class TestListSerializer(serializers.ModelSerializer):
    institute = InstituteListSerializer()

    class Meta:
        model=Test
        fields = ("id", "name", "status", "practice", "activation_time", "institute")

class TestCreateSerializer(serializers.ModelSerializer):        

    class Meta:
        model=Test
        fields = ("id", "name", "practice", "activation_time", "institute", "questions", "answers", "sections", "test_series", "exam")
        extra_kwargs = {'test_series': {'required': False}}

class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Payment
        fields =("transaction_id","receipt","user","amount","test_series")

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        exclude = ("registered_students",)

class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id','name','institute', 'status','practice','tags','date_added','activation_time','time_alotted','sections','questions')

class TestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id','name','institute','slug','status','practice','tags','date_added','activation_time','time_alotted')

class SessionSerializer(serializers.ModelSerializer):
    test = StudentTestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ('id', 'practice', 'response', 'test', 'checkin_time', 'duration', 'current', 'completed')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    test = StudentTestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ('id', 'test', 'marks', 'completed')

class ReviewSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ('id', 'response', 'test', 'result', 'marks', 'ranks')


class RankListSerializer(serializers.ModelSerializer):
    roll_number = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ('id', 'roll_number', 'name', 'ranks')

    def get_roll_number(self, obj):
        return Enrollment.objects.filter(student=obj.student, institute=obj.test.institute)[0].roll_number

    def get_name(self, obj):
        return obj.student.user.name

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
        fields = ("id", "institute", "batch", "roll_number", "joining_key")

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("id", "batch", "roll_number", "joining_key", "student")

class InstituteBatchSerializer(serializers.ModelSerializer):
    enrollments = BatchSerializer(many=True, required=False)
    class Meta:
        model = Batch
        fields = ("id", "name", "enrollments")

class BatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ("id", "name", "institute")

class FollowingInstitutesSerializer(serializers.ModelSerializer):
    batches = BatchListSerializer(many=True, read_only=True)
    user = UserListSerializer()
    enrollments = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ("id", "user", "batches", "enrollments")

    def get_enrollments(self, obj):
        return [enrollment.batch.id for enrollment in Enrollment.objects.filter(student=self.context['request'].user.student, institute=obj) if enrollment.batch]