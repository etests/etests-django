import json
import os
import sys
from datetime import date
from io import BytesIO
from random import choice, randint
from string import digits

import cv2
import numpy as np
from django.apps import apps
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import (
    APIException,
    MethodNotAllowed,
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import ResetCode
from .models import Institute
from ml.preprocessing import clean

from .forms import *
from .models import *
from .serializers import *
from .ses import send_email
from .utils import SessionEvaluation, generateRanks, getVirtualRanks

sensitive = method_decorator(
    sensitive_post_parameters("password", "old_password", "new_password")
)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @sensitive
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        data = {"user": user, "refresh": str(self.refresh), "access": str(self.access)}
        return JWTSerializer(data).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        send_email(user.email, "eTests Registration Successful", "Welcome to eTests.")

        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        user = serializer.create(self.request.data)
        self.refresh = RefreshToken.for_user(user)
        self.access = self.refresh.access_token
        return user


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("POST", "OPTIONS", "HEAD")

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data["user"]
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token

        if getattr(settings, "REST_SESSION_LOGIN", True):
            self.process_login()

    def get_response(self):
        serializer_class = JWTSerializer

        data = {
            "user": self.user,
            "refresh": str(self.refresh),
            "access": str(self.access),
        }

        serializer = serializer_class(instance=data, context={"request": self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, "ACCOUNT_LOGOUT_ON_GET", False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        return Response(
            {"detail": _("Logged out successfully.")}, status=status.HTTP_200_OK
        )


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()

        birth_date = self.request.data.get("birth_date", None)
        pincode = self.request.data.get("pincode", None)
        about = self.request.data.get("about", None)

        if instance.is_student and birth_date:
            instance.student.birth_date = birth_date
            instance.student.save()

        if instance.is_institute:
            if pincode:
                instance.institute.pincode = pincode
            instance.institute.about = about
            instance.institute.save()

        serializer.save()


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        return PasswordResetSerializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response("Password reset code sent.", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        return PasswordResetConfirmSerializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response("Password reset successful", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        return PasswordChangeSerializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response("Password changed successfully", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsInstituteOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_institute

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_institute
            and (not obj.institute or obj.institute == request.user.institute)
        )


class IsStudentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_student
            and (not obj.student or obj.student == request.user.student)
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


class BatchListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = BatchListSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return Batch.objects.filter(
                institute__in=self.request.user.student.institutes
            )
        elif self.request.user.is_institute:
            return Batch.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_staff:
            return Batch.objects.all()
        else:
            return None


class JoinedInstitutesView(generics.ListAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = JoinedInstitutesSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return Institute.objects.filter(
                students=self.request.user.student, verified=True
            )
        else:
            return None


class BatchListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = InstituteBatchSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Batch.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Batch.objects.all()
        else:
            return None

    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)


class BatchRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = InstituteBatchSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Batch.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Batch.objects.all()
        else:
            return None


class InstituteJoinView(APIView):
    permission_classes = (IsStudentOwner,)

    def post(self, request):
        roll_number = request.data["rollNumber"]
        joining_key = request.data["joiningKey"]
        try:
            enrollment = Enrollment.objects.get(
                roll_number=roll_number, joining_key=joining_key
            )
            enrollment.student = request.user.student
            enrollment.date_joined = datetime.now()
            enrollment.save()
            return Response("Joined Successfully")
        except:
            raise ParseError("Invalid roll number or joining key!")


class BatchJoinView(APIView):
    permission_classes = (IsStudentOwner,)

    def post(self, request):
        roll_number = request.data["rollNumber"]
        joining_key = request.data["joiningKey"]
        try:
            batch = Batch.objects.get(id=self.request.data["batch"])
            enrollment = Enrollment.objects.get(batch=batch, roll_number=roll_number)
            if enrollment.joining_key == joining_key:
                enrollment.student = request.user.student
                enrollment.date_joined = datetime.now()
                enrollment.save()
                # Feature required: Register this student to all the previous tests of this batch
                return Response("Joined Successfully")
            else:
                raise ParseError("Invalid roll number or joining key!")
        except:
            raise ParseError("Invalid roll number or joining key!")


class InstitutesListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Institute.objects.filter(verified=True, show=True)
        serializer = InstituteListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ExamListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Exam.objects.filter()
        serializer = ExamListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class SubjectListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Subject.objects.filter()
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)


class TopicListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Topic.objects.filter()
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data)


class TagListView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TestSeriesListView(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):
        return TestSeries.objects.filter(institute__verified=True, visible=True)


class TestSeriesListCreateView(generics.ListCreateAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return TestSeries.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_student:
            return TestSeries.objects.filter(
                registered_students=self.request.user.student,
                visible=True,
                institute__verified=True,
            )
        elif self.request.user.is_staff:
            return TestSeries.objects.all()
        return None

    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)


class TestSeriesRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return TestSeries.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return TestSeries.objects.all()
        else:
            return None


class TestListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_student:
            return StudentTestListSerializer
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
        else:
            return None


class FreeTestListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return StudentTestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
            return Test.objects.filter(
                free=True, sessions__student=self.request.user.student, visible=True
            ).distinct()
        else:
            return None


class TestCreateView(generics.CreateAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestCreateSerializer

    def perform_create(self, serializer):
        test_series_ids = self.request.data.pop("test_series", None)
        exam_id = self.request.data.get("exam", None)
        free = self.request.data.get("free", False)
        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
                for test_series_id in test_series_ids:
                    try:
                        test_series = TestSeries.objects.get(id=test_series_id)
                        test_series.exams.add(exam)
                        if test_series.price == 0:
                            free = True
                    except:
                        pass
            except Exception as e:
                pass
        batches = self.request.data.pop("batches", None)
        student_ids = []
        if batches:
            for batch_id in batches:
                try:
                    batch = Batch.objects.get(id=batch_id)
                    if batch.institute == self.request.user.institute:
                        student_ids += [student.id for student in batch.students()]
                except Exception as e:
                    pass
        serializer.save(
            institute=self.request.user.institute,
            registered_students=student_ids,
            free=free,
        )


class TestRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None


class SessionListView(generics.ListAPIView):
    permission_classes = (IsStudentOwner | permissions.IsAdminUser,)

    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Session.objects.filter(completed=True)
        elif self.request.user.is_student:
            return Session.objects.filter(
                student=self.request.user.student, completed=True
            )
        return None


class SessionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsStudentOwner | permissions.IsAdminUser,
    )

    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Session.objects.all()
        elif self.request.user.is_student:
            return Session.objects.filter(student=self.request.user.student)
        return None

    def create_session(self, test):
        response = []
        for i, question in enumerate(test.questions):
            answer = [[], [], [], []] if question["type"] == 3 else []
            status = 1 if i == 0 else 0
            response.append({"answer": answer, "status": status, "timeElapsed": 0})
        current = {"questionIndex": 0, "sectionIndex": 0}
        session = Session.objects.create(
            student=self.request.user.student,
            test=test,
            response=response,
            result=[],
            current=current,
            practice=(test.status > 1),
            duration=test.time_alotted,
        )
        return session

    def retrieve(self, *args, **kwargs):
        test_id = kwargs["test_id"]
        try:
            test = Test.objects.get(id=test_id)
        except:
            raise NotFound("This test does not exist.")
        try:
            session = Session.objects.get(
                test=test, student=self.request.user.student, completed=False
            )
            if test.status >= 2 and not session.practice:
                session.completed = True
                session.save()
                session = None
        except:
            session = None
        if session:
            if session.practice:
                self.serializer_class = PracticeSessionSerializer
            return Response(self.get_serializer(session).data)
        elif self.request.user.is_student:
            if self.request.user.student in test.registered_students.all() or test.free:
                sessions = Session.objects.filter(
                    test=test, student=self.request.user.student
                )
                if test.status == 0:
                    raise ParseError("This test is not active yet.")
                elif test.status == 1 and len(sessions) == 0 or test.status > 1:
                    session = self.create_session(test)
                elif test.status == 1 and len(sessions):
                    raise ParseError(
                        "You have already attempted this test. You can attempt this test in practice mode after result declaration."
                    )
            else:
                raise ParseError("You are not registered for this test.")
        else:
            raise PermissionDenied("You cannot attempt this test.")
        if session:
            if session.practice:
                self.serializer_class = PracticeSessionSerializer
            return Response(self.get_serializer(session).data)
        else:
            raise NotFound("Invalid Request.")

    def partial_update(self, *args, **kwargs):
        instance = self.get_object()
        session = self.request.data
        if session["practice"]:
            if instance.completed:
                raise PermissionDenied("You have already submitted this test.")
            else:
                self.serializer_class = PracticeSessionSerializer
                if instance.test.marks_list is not None:
                    instance.ranks = getVirtualRanks(
                        instance.test.marks_list, session["marks"]
                    )
        elif session["completed"]:
            self.serializer_class = ResultSerializer
            if instance.completed:
                raise PermissionDenied("You have already submitted this test.")
            else:
                test = Test.objects.get(id=instance.test.id)
                evaluated = SessionEvaluation(test, session).evaluate()
                instance.marks = evaluated[0]
                instance.result = {
                    "questionWiseMarks": evaluated[1],
                    "topicWiseMarks": evaluated[2],
                }
        serializer = self.get_serializer(instance, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


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
    permission_classes = (permissions.IsAdminUser,)

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
    generated = generateRanks(sessions)
    if generated:
        Session.objects.bulk_update(generated.get("sessions", None), ["ranks"])
        test.marks_list = generated.get("marks_list", None)
        test.stats = generated.get("stats", None)
        test.finished = True
        test.save()
        return True
    return False


class ResultView(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)

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


class Review(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
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
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)

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
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)

    def get(self, request, id):
        sessions = Session.objects.filter(
            test__id=id, completed=True, marks__isnull=False, ranks__isnull=False
        )
        serializer = RankListSerializer(sessions, many=True)
        return Response(serializer.data)


class TransactionListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Transaction.objects.filter(institute=self.request.user.institute)
        return None


class AITSTransactionListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = AITSTransactionSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return AITSTransaction.objects.filter(institute=self.request.user.institute)
        return None


class CreditListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = CreditUseSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return CreditUse.objects.filter(institute=self.request.user.institute)
        return None


class EnrollmentView(generics.ListCreateAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Enrollment.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_staff:
            return Enrollment.objects.all()
        return None

    def create(self, request, *args, **kwargs):
        enrollments = []
        headers = []
        data = [
            {
                "institute": request.user.institute.id,
                "batch": request.data["batch"],
                "roll_number": roll_number,
            }
            for roll_number in request.data["rollNumbers"]
        ]

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PaymentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            send_mail(
                payment.user.email,
                "Payment Verification in Progress",
                "Your payment of Rs."
                + str(payment.test_series.price)
                + " for "
                + payment.test_series.name
                + " will be verified shortly. The AITS will appear on your dashboard after payment is verified. If you have any query feel free to email us at help@etests.co.in",
            )
            return Response("Successful", status=status.HTTP_201_CREATED)
        else:
            raise ParseError("Invalid")


class EnrollmentRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Enrollment.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_student:
            return Enrollment.objects.filter(
                institute=self.request.user.student.institute
            )
        elif self.request.user.is_staff:
            return Enrollment.objects.all()
        else:
            return None


class AITSBuyer(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = AITSBuyerSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Payment.objects.filter(
                test_series__institute=self.request.user.institute,
                verified=True,
                show=True,
            )
        elif self.request.user.is_staff:
            return Payment.objects.filter(verified=True, show=True)
        else:
            return None


class PublishTestSeries(APIView):
    permission_classes = (permissions.IsAdminUser | IsInstituteOwner,)

    def post(self, request):
        try:
            instance = TestSeries.objects.get(id=request.data.get("id"))
            instance.visible = True
            instance.save()
            return Response(
                "AITS Published Sucessfully!", status=status.HTTP_201_CREATED
            )
        except:
            raise ParseError("Cannot publish this AITS.")


class UploadQuestionImageView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        uploaded_image = request.FILES.get("upload")
        raw_image = cv2.imdecode(
            np.fromstring(uploaded_image.read(), np.uint8), cv2.IMREAD_UNCHANGED
        )
        cleaned_image = clean(raw_image)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        _, image_buffer = cv2.imencode(".jpg", cleaned_image, encode_param)

        processed_image = SimpleUploadedFile(
            "question.jpg", BytesIO(image_buffer).getvalue()
        )

        if processed_image.size < uploaded_image.size:
            request.FILES["file"] = processed_image
        else:
            request.FILES["file"] = uploaded_image

        form = QuestionImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return JsonResponse(
                {"uploaded": 1, "fileName": image.file.name, "url": image.file.url}
            )
        else:
            return JsonResponse(
                {"uploaded": 0, "error": {"message": form.errors.as_text()}}
            )


class AddQuestionAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = QuestionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveQuestionAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = QuestionSerializer

    def post(self, request):
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
