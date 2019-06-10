from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.apps import apps

from .serializers import *

from .models import *
from authentication.models import Institute

class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class IsInstituteOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_institute and obj.institute == request.user.institute

class IsInstituteOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_institute

class IsStudentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_student and obj.institute == request.user.student      

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
    permission_classes = (IsInstituteOrReadOnly | permissions.IsAdminUser,)
    serializer_class = TestSeriesSerializer
    queryset = TestSeries.objects.all()
    

class TestSeriesRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner, permissions.IsAdminUser)
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
    permission_classes = (IsInstituteOrReadOnly | permissions.IsAdminUser,)
    serializer_class = TestSerializer
    queryset = Test.objects.all()
        
class TestRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner, permissions.IsAdminUser)
    serializer_class = TestSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None
        
class UnitTestListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsInstituteOrReadOnly | permissions.IsAdminUser,)
    serializer_class = UnitTestSerializer
    queryset = UnitTest.objects.all()
        
class UnitTestRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = UnitTestSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return UnitTest.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return UnitTest.objects.all()
        else:
            return None

class SessionListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Session.objects.filter()
        serializer = SessionSerializer(queryset, many=True)
        return Response(serializer.data)
        
class BuyerListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Buyer.objects.filter()
        serializer = BuyerSerializer(queryset, many=True)
        return Response(serializer.data)
        