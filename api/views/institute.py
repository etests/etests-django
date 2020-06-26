from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.permissions import IsStaff
from api.models import Institute, Contact, Batch
from api.permissions import IsStudentOwner, IsInstituteOwner, ReadOnly, IsStudent
from api.serializers.institute import *

from api.utils import get_client_country


class InstitutesListView(ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = InstituteListSerializer

    def get_queryset(self):
        queryset = Institute.objects.filter(verified=True, show=True)
        user = self.request.user
        if user.is_authenticated and user.country:
            queryset = queryset.filter(user__country=user.country)
        else:
            try:
                queryset = queryset.filter(
                    user__country=get_client_country(self.request)
                )
            except:
                pass
        return queryset


class InstitutesView(RetrieveUpdateAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | IsStaff,)
    serializer_class = InstituteDetailsSerializer
    lookup_field = "handle"
    allowed_methods = ("get", "patch")

    def get_queryset(self):
        return Institute.objects.filter(verified=True)


class JoinInstituteView(GenericAPIView):
    permission_classes = (IsStudent,)
    serializer_class = JoinInstituteSerializer

    def get_queryset(self):
        return Institute.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user.student)
        return Response({"id": instance.id}, status=status.HTTP_200_OK)


class ContactView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer


class BatchView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BatchSerializer
    filterset_fields = ("institute__handle",)
    queryset = Batch.objects.all()


# DEPRECATE
class JoinedInstitutesView(ListAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = JoinedInstitutesSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
            return self.request.user.student.institutes.filter(verified=True).distinct()
