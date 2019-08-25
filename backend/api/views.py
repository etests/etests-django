from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException, MethodNotAllowed, PermissionDenied, NotFound, ParseError
from django.apps import apps
from .utils import SessionEvaluation
from .serializers import *
from .models import *
from authentication.models import Institute

class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class IsInstituteOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_institute

    def has_object_permission(self, request, view, obj):
        return obj.institute == request.user.institute

class IsStudentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_student and obj.student == request.user.student

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and  obj.user == request.user

class InstitutesListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Institute.objects.filter()
        serializer = InstituteListSerializer(queryset, many=True)
        return Response(serializer.data)

class ExamListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Exam.objects.filter()
        serializer = ExamSerializer(queryset, many=True)
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
        
class TestSeriesListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
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


class TestListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            if self.request.user.is_student:
                return Test.objects.filter(institute__in=self.request.user.student.institutes.all())
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None

    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)
        
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

class SessionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudentOwner | permissions.IsAdminUser,)
    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Session.objects.all()
        elif self.request.user.is_student:
            return Session.objects.filter(student=self.request.user.student)
        return None

    def create_session(self, test):
        response = []
        for i in range(len(test.questions)):
            response.append({
                "answer": [],
                "status": 0,
                "timeElapsed": 0
            })
        current = {
            "questionIndex": 0,
            "sectionIndex": 0
        }    
        session = Session.objects.create(student=self.request.user.student, test=test, response=response, result=[], current=current)
        return session

    def retrieve(self, *args, **kwargs):
        test_id = kwargs['test_id']
        test=Test.objects.get(id=test_id)
        try:
            session = Session.objects.get(test=test, student=self.request.user.student, completed=False)
        except:
            session = None
        if(session):
            return Response(self.get_serializer(session).data)
        elif self.request.user.is_student:
            if self.request.user.student in test.registered_student.all():
                sessions = Session.objects.filter(test=test, student=self.request.user.student)
                if(len(sessions)==0 or test.practice):
                    session = self.create_session(test)
                else:
                    raise ParseError("You have already attempted this test.")
            else:
                raise ParseError("You are not registered for this test.")
        else:
            raise PermissionDenied("You cannot attempt this test.")
        if session:
            return Response(self.get_serializer(session).data)
        else:
            raise NotFound("Invalid Request.")
        

    def partial_update(self,*args,**kwargs):
        instance = self.get_object()
        session = self.request.data
        
        if session['completed']:
            if instance.completed:
                raise PermissionDenied("You have already submitted this test.")
            else:   
                test = Test.objects.get(id=instance.test.id)
                instance.marks = SessionEvaluation(test, session).evaluate()

        serializer = self.get_serializer(instance, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  

        return Response(serializer.data)

class ResultView(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = ResultSerializer
    def get_queryset(self):
        if self.request.user.is_institute:
            return Session.objects.filter(student__institutes = self.request.user.institute)
        if self.request.user.is_student:
            return Session.objects.filter(student = self.request.user.student)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

class Review(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = ResultSerializer
    def get_queryset(self):
        if self.request.user.is_institute:
            return Session.objects.filter(student__institutes = self.request.user.institute)
        if self.request.user.is_student:
            return Session.objects.filter(student = self.request.user.student)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        print(instance.result)
        if instance.result or len(instance.result)!=0:
            return Response(self.get_serializer(instance).data)
        else:
            raise ParseError("You cannot review this test yet.")
