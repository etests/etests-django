from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from api.permissions import IsStaff
from api.models import Batch, Exam, Test
from api.permissions import *
from api.serializers.test import (
    TestCreateUpdateSerializer,
    TestListSerializer,
    TestSerializer,
    TestEvaluationSerializer,
)
from rest_framework.response import Response
from rest_framework import status


class TestListCreateView(ListCreateAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | IsStaff,)
    filterset_fields = ("institute", "exam", "free")

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
                student = self.request.user.student
                return (
                    Test.objects.filter(aits=False, visible=True)
                    .filter(
                        Q(registered_students=student)
                        | Q(registered_batches__in=student.batches())
                    )
                    .distinct()
                )
            elif self.request.user.is_staff:
                return Test.objects.all()
        return None

    def perform_create(self, serializer):
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
    permission_classes = (IsInstituteOwner | IsStaff,)

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


class TestEvaluationView(GenericAPIView):
    permission_classes = (IsStaff,)
    serializer_class = TestEvaluationSerializer

    queryset = Test.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Successful", status=status.HTTP_200_OK)
