from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Session, Test
from api.permissions import (
    IsStudentOwner,
    IsInstituteOwner,
    IsRegisteredForTest,
    ReadOnly,
)
from api.serializers.session import SessionSerializer, RanksSerializer
from api.utils import SessionEvaluation, generate_ranks


class SessionListView(ListAPIView):
    permission_classes = (IsStudentOwner | IsAdminUser,)

    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Session.objects.filter(completed=True)
            elif self.request.user.is_student:
                return Session.objects.filter(
                    student=self.request.user.student, completed=True
                )


class SessionCreateRetrieveView(CreateAPIView, RetrieveAPIView):
    permission_classes = (IsRegisteredForTest,)
    serializer_class = SessionSerializer
    lookup_field = "test_id"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
            return Session.objects.filter(
                completed=False, student=self.request.user.student
            ).prefetch_related("test")

    def perform_create(self, serializer):
        serializer.save(
            student=self.request.user.student, test_id=self.kwargs.get("test_id")
        )


class SessionUpdateView(UpdateAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
            return Session.objects.filter(
                completed=False, student=self.request.user.student
            )


class ResultView(RetrieveAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)

    def get_serializer_class(self):
        return SessionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                return Session.objects.filter(student=self.request.user.student)
            elif self.request.user.is_institute:
                return Session.objects.filter(
                    test__institute=self.request.user.institute
                )
            elif self.request.user.is_staff:
                return Session.objects.all()


class RankListView(APIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)

    def get(self, request, id):
        sessions = Session.objects.filter(
            test__id=id, completed=True, marks__isnull=False, ranks__isnull=False
        )
        serializer = RanksSerializer(sessions, many=True)
        return Response(serializer.data)
