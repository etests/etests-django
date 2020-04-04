from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Test


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_staff


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsInstituteOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_institute

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_institute
            and (
                hasattr(obj, "institute")
                and obj.institute == request.user.institute
                or obj == request.user.institute
            )
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsStudentOwner(IsStudent):
    def has_object_permission(self, request, view, obj):
        return (
            self.has_permission(request, view)
            and not obj.student
            or obj.student == request.user.student
        )


class IsRegisteredForTest(IsStudentOwner):
    def has_permission(self, request, view):
        try:
            test_id = view.kwargs.get("test_id", None)
            test = Test.objects.get(id=test_id)
            return super().has_permission(request, view) and (
                request.user.student in test.registered_students.all()
                or (
                    not test.aits
                    and request.user.student in test.institute.students.all()
                )
                or test.free
            )
        except:
            return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user
