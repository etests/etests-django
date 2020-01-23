from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Session, Test
from api.permissions import *
from api.serializers.session import *
from api.utils import SessionEvaluation, generate_ranks


class SessionListView(ListAPIView):
    permission_classes = (IsStudentOwner | IsAdminUser,)

    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Session.objects.filter(completed=True)
        elif self.request.user.is_student:
            return Session.objects.filter(
                student=self.request.user.student, completed=True
            )
        return None


class SessionCreateRetrieveUpdateView(CreateAPIView, RetrieveUpdateAPIView):
    permission_classes = (IsRegisteredForTest,)
    serializer_class = SessionSerializer
    lookup_field = "test_id"
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        return Session.objects.filter(
            completed=False, student=self.request.user.student
        ).prefetch_related("test")

    def perform_create(self, serializer):
        serializer.save(
            student=self.request.user.student, test_id=self.kwargs.get("test_id")
        )


def evaluateLeftSessions(test):
    sessions = Session.objects.filter(test=test, practice=False, marks__isnull=True)
    for session in sessions:
        evaluated = SessionEvaluation(
            session.test, SessionSerializer(session).data
        ).evaluate()
        session.marks = evaluated[0]
        session.result = {
            "questionWiseMarks": evaluated[1],
            "topicWiseMarks": evaluated[2],
        }
        session.completed = True
    Session.objects.bulk_update(sessions, ["marks", "result", "completed"])


class EvaluateLeftSessions(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
            evaluateLeftSessions(test)
            return Response("Done!", status=status.HTTP_201_CREATED)
        except:
            raise ParseError("Some error ocurred")


def updateTestRanks(test):
    sessions = Session.objects.filter(test=test, practice=False)
    if len(sessions) == 0:
        test.finished = True
        test.save()
        return False
    generated = generate_ranks(sessions)
    if generated:
        Session.objects.bulk_update(generated.get("sessions", None), ["ranks"])
        test.marks_list = generated.get("marks_list", None)
        test.stats = generated.get("stats", None)
        test.finished = True
        test.save()
        return True
    return False


class ResultView(RetrieveAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)

    def get_serializer_class(self):
        session = self.get_object()
        test = session.test
        if session.practice or test.status > 1:
            return ReviewSerializer
        else:
            return ResultSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return Session.objects.filter(student=self.request.user.student)
        elif self.request.user.is_institute:
            return Session.objects.filter(test__institute=self.request.user.institute)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()

        if instance.marks is None:
            instance.completed = True
            evaluated = SessionEvaluation(
                instance.test, SessionSerializer(instance).data
            ).evaluate()
            instance.marks = evaluated[0]
            instance.result = {
                "questionWiseMarks": evaluated[1],
                "topicWiseMarks": evaluated[2],
            }
            instance.save()

        return Response(self.get_serializer(instance).data)


class Review(RetrieveAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Session.objects.filter(
                student__institutes=self.request.user.institute
            )
        if self.request.user.is_student:
            return Session.objects.filter(student=self.request.user.student)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        if instance.test.status > 1 and instance.result and len(instance.result) != 0:
            return Response(self.get_serializer(instance).data)
        else:
            raise ParseError("You cannot review this test yet.")


class GenerateRanks(APIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)

    def post(self, request, id):
        try:
            test = Test.objects.get(id=id)
        except Exception as e:
            print(e)
            raise NotFound("No such Test!")
        if test.practice:
            raise PermissionDenied("Ranks cannot be generated for this test.")
        if test.status <= 1:
            raise PermissionDenied("Ranks can be generated only after test closes.")
        elif test.status in [2, 3] or request.user.is_staff:
            evaluateLeftSessions(test)
            updateTestRanks(test)
            return Response("Ranks generated.", status=status.HTTP_201_CREATED)
        else:
            raise ParseError("Final ranks are already declared.")


class RankListView(APIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)

    def get(self, request, id):
        sessions = Session.objects.filter(
            test__id=id, completed=True, marks__isnull=False, ranks__isnull=False
        )
        serializer = RankListSerializer(sessions, many=True)
        return Response(serializer.data)
