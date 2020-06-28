from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateAPIView

from api.models import Enrollment
from api.permissions import IsInstituteOwner, ReadOnly, IsStudentOwner
from api.serializers.enrollment import *


class EnrollmentListCreateView(ListCreateAPIView):
    permission_classes = (IsStudentOwner,)
    filterset_fields = ("institute", "institute__handle")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StudentEnrollmentListSerializer
        else:
            return StudentEnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                return Enrollment.objects.filter(student=self.request.user.student)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)


class EnrollmentDeleteView(DestroyAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = StudentEnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                return Enrollment.objects.filter(student=self.request.user.student)

    def perform_update(self, serializer):
        serializer.save(student=self.request.user.student)


class EnrollmentView(ListAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Enrollment.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Enrollment.objects.all()


class EnrollmentRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Enrollment.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_student:
                return Enrollment.objects.filter(
                    institute__in=self.request.user.student.institutes.all()
                )
            elif self.request.user.is_staff:
                return Enrollment.objects.all()
