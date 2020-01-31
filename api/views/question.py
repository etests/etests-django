from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Question
from api.serializers.common import QuestionSerializer


class AddQuestionAPIView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveQuestionAPIView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer

    def get(self, request):
        params = request.data
        type = params.get("type", None)
        difficulty = params.get("difficulty", None)
        subject_index = params.get("subject_index", None)
        topic_index = params.get("topic_index", None)

        questions = Question.objects.all()
        if type:
            questions = questions.filter(type=type)
        if difficulty:
            questions = questions.filter(difficulty=difficulty)
        if subject_index:
            questions = questions.filter(subject_index=subject_index)
            if topic_index:
                questions = questions.filter(topic_index=topic_index)

        try:
            count = questions.count()
            serializer = self.serializer_class(questions[randint(0, count - 1)])
            return Response(serializer.data)
        except:
            raise NotFound("No matching question!")
