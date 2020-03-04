from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateUpdateAPIView
from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Question
from api.serializers.common import QuestionSerializer


class AllowPOSTforAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.method in (*SAFE_METHODS, "PATCH")
        return False


class QuestionView(ListBulkCreateUpdateAPIView):
    permission_classes = (AllowPOSTforAdminOnly,)
    serializer_class = QuestionSerializer
    filterset_fields = ("type", "difficulty", "subject_index", "topic_index")

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Question.objects.all()
        else:
            return Question.objects.filter(
                Q(subject_index__isnull=True)
                | Q(topic_index__isnull=True)
                | Q(difficulty__isnull=True)
                | Q(type__isnull=True)
            )
