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
        queryset =  Institute.objects.filter(verified=True, show=True)
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user__country=user.country)
        else:
            try:
                queryset = queryset.filter(
                    user__country__name=get_client_country(self.request)
                )
            except:
                pass
        return queryset


# DEPRECATE
class JoinedInstitutesView(ListAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = JoinedInstitutesSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return self.request.user.student.institutes.filter(verified=True).distinct()
        else:
            return None
