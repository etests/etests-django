from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.models import Batch, Exam, Test
from api.permissions import *
from api.serializers.test import (
    TestSerializer,
    TestListSerializer,
    TestCreateSerializer,
)


class TestListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["institute"]

    def get_serializer_class(self):
        return TestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(
                    aits=False, institute=self.request.user.institute
                )
            elif self.request.user.is_student:
                return Test.objects.filter(
                    aits=False,
                    registered_students=self.request.user.student,
                    visible=True,
                )
            elif self.request.user.is_staff:
                return Test.objects.all()
        return None


class FreeTestListView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return TestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
            return Test.objects.filter(
                free=True, sessions__student=self.request.user.student, visible=True
            ).distinct()
        else:
            return None


class TestCreateView(CreateAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = TestCreateSerializer

    def perform_create(self, serializer):
        # TODO: Add exams property to TestSeries
        # TODO: Add registered_batches field to Test
        serializer.save(institute=self.request.user.institute)


class TestRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = TestSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Test.objects.all()
        return None
