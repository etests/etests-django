from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes=[JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes=[IsAdminUser, IsOwnerOrReadOnly]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class InstituteViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }