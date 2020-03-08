from django.http import JsonResponse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.forms import ImageUploadForm
from api.models import (
    Exam,
    Image,
    Payment,
    ResetCode,
    Subject,
    TestSeriesTransaction,
    Topic,
    Transaction,
    TestSeries,
)
from api.permissions import IsInstituteOwner, IsStudent, ReadOnly
from api.serializers.common import *
from api.serializers.exam import *
from api.utils import clean_image, get_client_country
from django.shortcuts import get_object_or_404
from django.http.response import Http404


class ExamListView(ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = ExamSerializer

    def get_queryset(self):
        queryset = Exam.objects.all()
        user = self.request.user
        if user.is_authenticated and user.country:
            queryset = queryset.filter(countries__contains=user.country)
        else:
            try:
                queryset = queryset.filter(
                    countries__contains=get_client_country(self.request)
                )
            except:
                pass
        return queryset


class TopicListView(ListCreateAPIView):
    permission_classes = (ReadOnly | IsAdminUser,)
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class SubjectListView(ListCreateAPIView):
    permission_classes = (ReadOnly | IsAdminUser,)
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class TransactionListView(ListAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_institute:
            return Transaction.objects.filter(institute=self.request.user.institute)


class TestSeriesTransactionListView(ListAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = TestSeriesTransactionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_institute:
            return TestSeriesTransaction.objects.filter(
                institute=self.request.user.institute
            )


class CreditListView(ListAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = CreditUseSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_institute:
            return CreditUse.objects.filter(institute=self.request.user.institute)


class PaymentView(UpdateAPIView):
    permission_classes = (IsStudent,)
    serializer_class = PaymentSerializer
    lookup_field = "transaction_id"
    allowed_methods = ("patch",)

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response("Invalid Transaction Id", status=status.HTTP_404_NOT_FOUND)

        return super(PaymentView, self).handle_exception(exc)

    def get_queryset(self):
        return Payment.objects.filter(student__isnull=True)

    def perform_update(self, serializer):
        serializer.save(student=self.request.user.student)


class PaymentGatewayView(CreateAPIView):
    permission_classes = (IsStudent,)
    serializer_class = PaymentGatewaySerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)


class TestSeriesBuyersView(ListAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = PaymentListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Payment.objects.filter(
                    test_series__institute=self.request.user.institute,
                    verified=True,
                    show=True,
                )
            elif self.request.user.is_staff:
                return Payment.objects.filter(verified=True, show=True)


class UploadImageView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        uploaded_image = request.FILES.get("upload")

        processed_image = clean_image(uploaded_image)

        if processed_image.size < uploaded_image.size:
            request.FILES["file"] = processed_image
        else:
            request.FILES["file"] = uploaded_image

        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return JsonResponse(
                {"uploaded": 1, "file_name": image.file.name, "url": image.file.url}
            )
        else:
            return JsonResponse(
                {"uploaded": 0, "error": {"message": form.errors.as_text()}}
            )
