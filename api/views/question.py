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
        subjectIndex = params.get("subjectIndex", None)
        topicIndex = params.get("topicIndex", None)

        questions = Question.objects.all()
        if type:
            questions = questions.filter(type=type)
        if difficulty:
            questions = questions.filter(difficulty=difficulty)
        if subjectIndex:
            questions = questions.filter(subjectIndex=subjectIndex)
            if topicIndex:
                questions = questions.filter(topicIndex=topicIndex)

        try:
            count = questions.count()
            serializer = self.serializer_class(questions[randint(0, count - 1)])
            return Response(serializer.data)
        except:
            raise NotFound("No matching question!")
