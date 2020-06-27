from api.serializers.batch import *
from rest_framework import permissions, generics
from api.permissions import *
from api.models import Batch, Institute
from rest_framework import status
from rest_framework.response import Response


class BatchListView(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = BatchSerializer
    filterset_fields = ("institute", "institute__handle")

    def get_queryset(self):
        return Batch.objects.all()


class BatchListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = BatchEnrollmentsSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Batch.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Batch.objects.all()

    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)


class BatchRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = BatchEnrollmentsSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Batch.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Batch.objects.all()

