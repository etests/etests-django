from api.serializers.batch import *
from rest_framework import permissions, generics
from api.permissions import *
from api.models import Batch, Institute
from rest_framework import status
from rest_framework.response import Response



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


class BatchJoinView(generics.GenericAPIView):
    permission_classes = (IsStudent,)
    serializer_class = BatchJoinSerializer

    def get_queryset(self):
        return Batch.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Batch Joined Successfully", status=status.HTTP_200_OK)

