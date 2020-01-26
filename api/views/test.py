from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS

from api.models import Batch, Exam, Test
from api.permissions import *
from api.serializers.test import (
    TestSerializer,
    TestListSerializer,
    TestCreateUpdateSerializer,
)


class TestListCreateView(ListCreateAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | IsAdminUser,)
    filterset_fields = ["institute"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TestCreateUpdateSerializer
        else:
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

    def perform_create(self, serializer):
        # TODO: Add exams property to TestSeries
        # TODO: Add registered_batches field to Test
        serializer.save(institute=self.request.user.institute)


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


class TestRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TestSerializer
        else:
            return TestCreateUpdateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"allow_answers": True})
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Test.objects.all()
        return None
