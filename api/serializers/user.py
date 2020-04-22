from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from api.models import User


class UserSerializer(ModelSerializer):
    birth_date = SerializerMethodField()
    pincode = SerializerMethodField()
    about = SerializerMethodField()
    country = StringRelatedField()
    scope = SerializerMethodField()
    handle = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "city",
            "state",
            "country",
            "birth_date",
            "pincode",
            "image",
            "about",
            "scope",
            "handle",
        )

    def get_scope(self, obj):
        scope = []
        if obj.is_student:
            scope.append("student")
        if obj.is_institute:
            scope.append("institute")
        if obj.is_staff:
            scope.append("staff")
        return scope

    def get_birth_date(self, obj):
        if obj.is_student:
            return obj.student.birth_date
        return None

    def get_pincode(self, obj):
        if obj.is_institute:
            return obj.institute.pincode
        return None

    def get_about(self, obj):
        if obj.is_institute:
            return obj.institute.about
        return None

    def get_handle(self, obj):
        if obj.is_institute:
            return obj.institute.handle
        return None
