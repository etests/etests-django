from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateUpdateAPIView
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import UpdateAPIView

from api.models import Question
from api.serializers.common import QuestionSerializer, QuestionAnnotateSerializer


class AllowPOSTforAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.method in SAFE_METHODS
        return False


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
    filterset_fields = ("type", "difficulty", "subject_index", "topic_index")
    allowed_methods = (*SAFE_METHODS, "POST", "PATCH")

    def get_serializer_class(self):
        return QuestionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Question.objects.all()
        else:
            return Question.objects.filter(
                Q(type__isnull=True)
                | Q(difficulty__isnull=True)
                | Q(subject_index__isnull=True)
                | Q(topic_index__isnull=True)
            )


class QuestionUpdateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    pagination_class = Pagination
    filterset_fields = ("type", "difficulty", "subject_index", "topic_index")
    allowed_methods = ("PATCH",)

    def get_serializer_class(self):
        return QuestionAnnotateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Question.objects.all()
        else:
            return Question.objects.filter(
                Q(type__isnull=True)
                | Q(difficulty__isnull=True)
                | Q(subject_index__isnull=True)
                | Q(topic_index__isnull=True)
            )
