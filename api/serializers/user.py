from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from api.models import User, Institute, Student


class InstituteDetailsSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = ("id", "handle", "pincode", "about")


class StudentDetailsSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ProfileSerializer(ModelSerializer):
    birth_date = SerializerMethodField(read_only=True)
    pincode = SerializerMethodField(read_only=True)
    country = StringRelatedField()

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "phone",
            "city",
            "state",
            "country",
            "birth_date",
            "pincode",
            "image",
        )

    def get_birth_date(self, obj):
        if obj.is_student:
            return obj.student.birth_date
        return None

    def get_pincode(self, obj):
        if obj.is_institute:
            return obj.institute.pincode
        return None


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "city", "state", "image")


class UserDetailsSerializer(ModelSerializer):
    profile = ProfileSerializer(source="*")
    details = SerializerMethodField()
    type = SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "type", "profile", "details")
        read_only_fields = ("id", "email")

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
