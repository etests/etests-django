from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.models import Enrollment
from api.permissions import IsInstituteOwner, ReadOnly
from api.serializers.enrollment import *


class EnrollmentView(ListCreateAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Enrollment.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_staff:
            return Enrollment.objects.all()
        return None

    def create(self, request, *args, **kwargs):
        enrollments = []
        headers = []
        data = [
            {
                "institute": request.user.institute.id,
                "batch": request.data["batch"],
                "roll_number": roll_number,
            }
            for roll_number in request.data["roll_numbers"]
        ]

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class EnrollmentRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Enrollment.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_student:
            return Enrollment.objects.filter(
                institute=self.request.user.student.institute
            )
        elif self.request.user.is_staff:
            return Enrollment.objects.all()
        else:
            return None
