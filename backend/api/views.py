from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import InstituteListSerializr
from authentication.models import Institute

class InstitutesListView(viewsets.ViewSet):
    """
    displays a list of all Institute objects
    """
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = Institute.objects.filter()
        serializer = InstituteListSerializr(queryset, many=True)
        return Response(serializer.data)