from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.models import Institute
from api.permissions import IsStudentOwner, ReadOnly
from api.serializers.institute import *


class InstitutesListView(ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = InstituteListSerializer

    def get_queryset(self):
        return Institute.objects.filter(verified=True, show=True)

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
