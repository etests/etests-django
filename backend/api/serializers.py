from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from authentication.models import *
from .models import *
from authentication.serializers import UserDetailsSerializer, StudentDetailsSerializer, InstituteDetailsSerializer

class TestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("id","name", "status", "date_added", "activation_time", "closing_time", "time_alotted")

class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "practice", "checkin_time", "completed")

class StudentTestListSerializer(serializers.ModelSerializer):
    institute = serializers.SerializerMethodField()
    sessions = serializers.SerializerMethodField()
    
    class Meta:
        model = Test
        fields = ("id","name","institute", "status", "aits", "date_added", "activation_time", "closing_time",  "time_alotted", "sessions")
    
    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

    def get_sessions(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated and user.is_student:
            serializer_context = {"request": self.context.get("request") }
            sessions =  Session.objects.filter(test=obj, student=user.student)
            return SessionListSerializer(sessions, many=True, read_only=True, context = serializer_context).data
        else:
            return None


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        if not self.context["request"].user.is_authenticated or self.context["request"].user.is_student:
            data = data.filter(institute__verified = True, visible = True)
        elif self.context["request"].user.is_staff:
            pass
        elif self.context["request"].user.is_institute:
            data = data.filter(institute = self.context["request"].user.institute)
        
        return super(FilteredListSerializer, self).to_representation(data)

class TestSeriesSerializer(serializers.ModelSerializer):
    tests = serializers.SerializerMethodField()
    institute = serializers.SerializerMethodField()
    exams = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = TestSeries
        fields = ("id", "name", "price", "visible", "exams", "tests", "institute", "status")

    def get_tests(self, obj):
        serializer_context = {"request": self.context.get("request") }
        tests = obj.tests
        serializer = StudentTestListSerializer(tests, many=True, read_only=True, context=serializer_context)
        return serializer.data

    def get_status(self, obj):
        if not self.context["request"].user.is_authenticated:
            return 0
        elif not self.context["request"].user.is_student:
            return 1
        else:
            payments = Payment.objects.filter(user = self.context["request"].user, test_series = obj)
            if len(payments) > 0:
                if payments[0].verified:
                    return 4
                else:
                    return 3
            else:
                return 2

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

    def get_exams(self, obj):
        return [exam.name for exam in obj.exams.all()]

class BatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ("id", "name", "institute")

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "city", "state")

class InstituteListSerializer(serializers.ModelSerializer):
    batches = BatchListSerializer(many=True, read_only=True)
    user = UserListSerializer()
    test_series = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ("id", "user", "pincode", "test_series", "batches")

    def get_test_series(self, obj):
        serializer_context = {"request": self.context.get("request") }
        test_series = obj.test_series.filter(institute__verified=True, visible=True)
        serializer = TestSeriesSerializer(test_series, many=True, context=serializer_context)
        return serializer.data

class ExamListSerializer(serializers.ModelSerializer):
    test_series = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ("id", "name", "start_date", "test_series", "image")
    
    def get_test_series(self, obj):
        serializer_context = {"request": self.context.get("request") }
        test_series = obj.test_series.filter(institute__verified=True, visible=True)
        serializer = TestSeriesSerializer(test_series, many=True, context=serializer_context)
        return serializer.data

class TestListSerializer(serializers.ModelSerializer):
    institute = InstituteListSerializer()

    class Meta:
        model=Test
        fields = ("id", "name", "status", "aits", "activation_time", "closing_time", "institute")

class TestCreateSerializer(serializers.ModelSerializer):        

    class Meta:
        model=Test
        fields = ("id", "name", "aits", "activation_time", "closing_time","time_alotted", "institute", "questions", "answers", "sections", "test_series", "exam", "status")
        extra_kwargs = {"test_series": {"required": False}, "status": {"read_only": True}}

class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Payment
        fields =("transaction_id","receipt","user","amount","test_series")

class AITSBuyerSerializer(serializers.ModelSerializer):
    test_series = serializers.SerializerMethodField()
    class Meta:
        model=Payment
        fields = ("test_series","date_added")
    
    def get_test_series(self, obj):
        return {
            "id": obj.test_series.id,
            "name": obj.test_series.name
        }

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        exclude = ("registered_students","marks_list")

class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("id","name","institute", "status","aits","tags","date_added","activation_time", "closing_time", "time_alotted","sections","questions")

class TestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("id","name","institute","slug","status","aits","tags","date_added","activation_time", "closing_time",  "time_alotted")

class SessionSerializer(serializers.ModelSerializer):
    test = StudentTestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ("id", "practice", "response", "test", "checkin_time", "duration", "current", "completed")

class PracticeSessionSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ("id", "practice", "response", "test", "checkin_time", "duration", "current", "completed", "result", "marks", "ranks")
        extra_kwargs = {"ranks": {"read_only": True}}



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
    test = StudentTestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ("id", "response", "test", "marks", "completed")

class ReviewSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = Session
        fields = ("id", "response", "test", "result", "marks", "completed", "ranks")


class RankListSerializer(serializers.ModelSerializer):
    roll_number = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ("id", "roll_number", "name", "ranks")

    def get_roll_number(self, obj):
        try:
            return Enrollment.objects.get(student=obj.student, institute=obj.test.institute).roll_number
        except:
            return obj.student.id

    def get_name(self, obj):
        return obj.student.user.name

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("__all__")

class CreditUseSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField("get_test_name")

    class Meta:
        model = CreditUse
        fields = ("__all__")

    def get_test_name(self, obj):
        return obj.test.name

class AITSTransactionSerializer(serializers.ModelSerializer):
    test_series = serializers.SerializerMethodField()
    class Meta:
        model = AITSTransaction
        fields = ("__all__")


    def get_test_series(self, obj):
        return ", ".join([test_series.name for test_series in obj.test_series.all()])

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

class JoinedInstitutesSerializer(serializers.ModelSerializer):
    batches = BatchListSerializer(many=True, read_only=True)
    user = UserListSerializer()
    enrollments = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ("id", "user", "batches", "enrollments")

    def get_enrollments(self, obj):
        return [enrollment.batch.id for enrollment in Enrollment.objects.filter(student=self.context["request"].user.student, institute=obj) if enrollment.batch]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("__all__")
        extra_kwargs = {"id": {"read_only": True}}