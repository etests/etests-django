from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateUpdateAPIView

from api.models import Question
from api.serializers.common import QuestionSerializer


class QuestionView(ListBulkCreateUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer
    filterset_fields = ("type", "difficulty", "subject_index", "topic_index")

    def get_queryset(self):
        return Question.objects.all()
