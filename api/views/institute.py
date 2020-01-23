from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import Institute
from api.permissions import IsStudentOwner, ReadOnly
from api.serializers.institute import *


class InstitutesListView(ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Institute.objects.filter(verified=True, show=True)
        serializer = InstituteListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


# DEPRECATE
class JoinedInstitutesView(ListAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = JoinedInstitutesSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return Institute.objects.filter(
                students=self.request.user.student, verified=True
            )
        else:
            return None
