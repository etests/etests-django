from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    BasePermission,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateUpdateAPIView

from api.models import Question
from api.serializers.common import QuestionAnnotateSerializer, QuestionSerializer


class AllowPOSTforAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
            or request.method in SAFE_METHODS
        )


class Pagination(PageNumberPagination):
    page_size = 20

    def get_next_link(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()


class QuestionView(ListBulkCreateUpdateAPIView):
    permission_classes = (AllowPOSTforAdminOnly,)
    pagination_class = Pagination
    filterset_fields = ("type", "difficulty", "subject", "topic")
    allowed_methods = (*SAFE_METHODS, "POST", "PATCH")

    def get_serializer_class(self):
        return QuestionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Question.objects.filter(institute__isnull=True)
        else:
            return (
                Question.objects.filter(institute__isnull=True)
                .filter(Q(subject__isnull=True) | Q(topic__isnull=True))
                .order_by("?")
            )


class QuestionUpdateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    filterset_fields = ("type", "difficulty", "subject", "topic")
    allowed_methods = ("PATCH",)

    def get_serializer_class(self):
        return QuestionAnnotateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Question.objects.filter(institute__isnull=True)
        else:
            return Question.objects.filter(institute__isnull=True).filter(
                Q(subject__isnull=True) | Q(topic__isnull=True)
            )
