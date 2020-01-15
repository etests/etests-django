from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsInstituteOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_institute

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_institute
            and (not obj.institute or obj.institute == request.user.institute)
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsStudentOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_student
            and (not obj.student or obj.student == request.user.student)
        )


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user

