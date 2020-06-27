from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateAPIView

from api.models import Enrollment
from api.permissions import IsInstituteOwner, ReadOnly
from api.serializers.enrollment import *


class EnrollmentView(ListBulkCreateUpdateAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Enrollment.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Enrollment.objects.all()

    def perform_bulk_create(self, serializer):
        if self.request.user.is_institute:
            serializer.save(institute=self.request.user.institute)
        elif self.request.user.is_staff:
            serializer.save()


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
