from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as validators
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from .forms import PasswordResetForm, SetPasswordForm
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "password", "is_student", "is_institute")
        extra_kwargs = {"phone": {"required": False}}

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address.")
            )
        return email

    def validate_password(self, password):
        errors = dict()
        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        if user.is_student:
            Student.objects.create(user=user)
        elif user.is_institute:
            Institute.objects.create(user=user)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def _validate_username(self, username, password):
        user = None
        instance = (
            User.objects.filter(email=username).first()
            or User.objects.filter(phone=username).first()
        )
        if instance:
            user = self.authenticate(email=instance.email, password=password)
        else:
            msg = _("No user with this email/password.")
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = None

        user = self._validate_username(username, password)

        if user:
            if not user.is_active:
                msg = _("User account is disabled.")
                raise exceptions.ValidationError(msg)
        else:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return attrs


class InstituteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"


class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField(read_only=True)
    pincode = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "phone", "city", "state", "birth_date", "pincode")

    def get_birth_date(self, obj):
        if obj.is_student:
            return obj.student.birth_date
        return None

    def get_pincode(self, obj):
        if obj.is_institute:
            return obj.institute.pincode
        return None


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source="*")
    details = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "type", "profile", "details")
        read_only_fields = ("email",)

    def get_type(self, obj):
        if obj.is_student:
            return "student"
        elif obj.is_institute:
            return "institute"
        elif obj.is_staff:
            return "staff"
        return ""

    def get_details(self, obj):
        if obj.is_student:
            return StudentDetailsSerializer(obj.student, context=self.context).data
        elif obj.is_institute:
            return InstituteDetailsSerializer(obj.institute, context=self.context).data
        else:
            return None


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """

    refresh = serializers.CharField()
    access = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserDetailsSerializer(obj["user"], context=self.context).data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get("request")
        self.reset_form.save(from_email=getattr(settings, "EMAIL_ID"))


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    reset_code = serializers.CharField()
    new_password = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        try:
            self.reset_code_instance = ResetCode.objects.get(
                reset_code=attrs.get("reset_code"), done=False, date_added=date.today()
            )
            self.user = self.reset_code_instance.user
        except Exception as e:
            print(e)
            raise ValidationError({"reset_code": ["Invalid reset code"]})

        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        self.reset_code_instance.done = True
        self.reset_code_instance.save()
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = True
        self.logout_on_password_change = False
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop("old_password")

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            err_msg = _(
                "Your old password was entered incorrectly. Please enter it again."
            )
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(self.request, self.user)


class TestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "status",
            "date_added",
            "activation_time",
            "closing_time",
            "time_alotted",
        )


class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "practice", "checkin_time", "completed")


class StudentTestListSerializer(serializers.ModelSerializer):
    institute = serializers.SerializerMethodField()
    sessions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "institute",
            "status",
            "aits",
            "date_added",
            "activation_time",
            "closing_time",
            "time_alotted",
            "sessions",
            "free",
            "syllabus",
        )

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}

    def get_sessions(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated and user.is_student:
            serializer_context = {"request": self.context.get("request")}
            sessions = Session.objects.filter(test=obj, student=user.student)
            return SessionListSerializer(
                sessions, many=True, read_only=True, context=serializer_context
            ).data
        else:
            return None


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if (
            not self.context["request"].user.is_authenticated
            or self.context["request"].user.is_student
        ):
            data = data.filter(institute__verified=True, visible=True)
        elif self.context["request"].user.is_staff:
            pass
        elif self.context["request"].user.is_institute:
            data = data.filter(institute=self.context["request"].user.institute)

        return super(FilteredListSerializer, self).to_representation(data)


class TestSeriesSerializer(serializers.ModelSerializer):
    tests = serializers.SerializerMethodField()
    institute = serializers.SerializerMethodField()
    exams = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = TestSeries
        fields = (
            "id",
            "name",
            "price",
            "visible",
            "exams",
            "tests",
            "institute",
            "status",
        )

    def get_tests(self, obj):
        serializer_context = {"request": self.context.get("request")}
        tests = obj.tests
        serializer = StudentTestListSerializer(
            tests, many=True, read_only=True, context=serializer_context
        )
        return serializer.data

    def get_status(self, obj):
        if not self.context["request"].user.is_authenticated:
            return 0
        elif not self.context["request"].user.is_student:
            return 1
        else:
            payments = Payment.objects.filter(
                user=self.context["request"].user, test_series=obj
            )
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
        fields = ("id", "user", "pincode", "test_series", "batches", "rating", "about")

    def get_test_series(self, obj):
        serializer_context = {"request": self.context.get("request")}
        test_series = obj.test_series.filter(institute__verified=True, visible=True)
        serializer = TestSeriesSerializer(
            test_series, many=True, context=serializer_context
        )
        return serializer.data


class ExamListSerializer(serializers.ModelSerializer):
    test_series = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ("id", "name", "start_date", "test_series", "image", "position")

    def get_test_series(self, obj):
        serializer_context = {"request": self.context.get("request")}
        test_series = obj.test_series.filter(institute__verified=True, visible=True)
        serializer = TestSeriesSerializer(
            test_series, many=True, context=serializer_context
        )
        return serializer.data


class TestListSerializer(serializers.ModelSerializer):
    institute = serializers.SerializerMethodField()
    exam = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "status",
            "aits",
            "activation_time",
            "closing_time",
            "time_alotted",
            "institute",
            "exam",
            "free",
            "syllabus",
        )

    def get_exam(self, obj):
        if obj.exam is not None:
            return obj.exam.name
        else:
            return ""

    def get_institute(self, obj):
        return {"id": obj.institute.id, "name": obj.institute.user.name}


class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "aits",
            "activation_time",
            "closing_time",
            "time_alotted",
            "institute",
            "questions",
            "answers",
            "sections",
            "test_series",
            "exam",
            "status",
            "free",
            "syllabus",
        )
        extra_kwargs = {
            "test_series": {"required": False},
            "status": {"read_only": True},
        }


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("transaction_id", "receipt", "user", "amount", "test_series")


class AITSBuyerSerializer(serializers.ModelSerializer):
    test_series = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("test_series", "date_added")

    def get_test_series(self, obj):
        return {"id": obj.test_series.id, "name": obj.test_series.name}


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        exclude = ("registered_students", "marks_list")


class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "institute",
            "status",
            "aits",
            "tags",
            "date_added",
            "activation_time",
            "closing_time",
            "time_alotted",
            "sections",
            "questions",
            "free",
            "syllabus",
        )


class TestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "institute",
            "slug",
            "status",
            "aits",
            "tags",
            "date_added",
            "activation_time",
            "closing_time",
            "time_alotted",
            "free",
            "syllabus",
        )


class SessionSerializer(serializers.ModelSerializer):
    test = StudentTestSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = (
            "id",
            "practice",
            "response",
            "test",
            "checkin_time",
            "duration",
            "current",
            "completed",
        )


class PracticeSessionSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = (
            "id",
            "practice",
            "response",
            "test",
            "checkin_time",
            "duration",
            "current",
            "completed",
            "result",
            "marks",
            "ranks",
        )
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
        fields = ("id", "roll_number", "name", "marks", "ranks", "practice")

    def get_roll_number(self, obj):
        try:
            return Enrollment.objects.get(
                student=obj.student, institute=obj.test.institute
            ).roll_number
        except:
            return "-"

    def get_name(self, obj):
        return obj.student.user.name


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CreditUseSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField("get_test_name")

    class Meta:
        model = CreditUse
        fields = "__all__"

    def get_test_name(self, obj):
        return obj.test.name


class AITSTransactionSerializer(serializers.ModelSerializer):
    test_series = serializers.SerializerMethodField()

    class Meta:
        model = AITSTransaction
        fields = "__all__"

    def get_test_series(self, obj):
        return ", ".join([test_series.name for test_series in obj.test_series.all()])


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = (
            "id",
            "institute",
            "batch",
            "roll_number",
            "joining_key",
            "student",
            "date_joined",
        )
        read_only_fields = ("student", "date_joined")


class BatchJoinSerializer(serializers.Serializer):
    roll_number = serializers.CharField()
    joining_key = serializers.CharField()

    def validate(self, attrs):
        try:
            enrollment = self.instance.enrollments.get(
                roll_number=attrs["roll_number"], joining_key=attrs["joining_key"]
            )
        except Enrollment.DoesNotExist:
            raise serializers.ValidationError("Invalid roll number or joining key")

        if enrollment.student is not None:
            raise serializers.ValidationError("This joining key has been already used")
        else:
            self.enrollment = enrollment

        return attrs

    def save(self):
        self.enrollment.student = self.context.get("request").user.student
        self.enrollment.date_joined = datetime.now()
        self.enrollment.save()


class InstituteBatchSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, required=False)

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
        return [
            enrollment.batch.id
            for enrollment in Enrollment.objects.filter(
                student=self.context["request"].user.student, institute=obj
            )
            if enrollment.batch
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}
