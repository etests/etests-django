from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser

from api.models import TestSeries
from api.permissions import *
from api.serializers.testseries import TestSeriesSerializer

from api.utils import get_client_country


class TestSeriesListView(ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = TestSeriesSerializer

    filterset_fields = ("institute", "exams")

    def get_queryset(self):
        queryset = TestSeries.objects.filter(
            institute__verified=True, visible=True
        ).exclude(tests=None)
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(institute__user__country=user.country)
        else:
            try:
                queryset = queryset.filter(
                    institute__user__country__name=get_client_country(self.request)
                )
            except:
                pass
        return queryset


class TestSeriesListCreateView(ListCreateAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | IsAdminUser,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return TestSeries.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_student:
            return TestSeries.objects.filter(
                registered_students=self.request.user.student,
                visible=True,
                institute__verified=True,
            )
        elif self.request.user.is_staff:
            return TestSeries.objects.all()
        return None

    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)


class TestSeriesRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return TestSeries.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return TestSeries.objects.all()
        return None
