from django.http import JsonResponse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.forms import PaymentForm, ImageUploadForm
from api.models import (
    TestSeriesTransaction,
    Exam,
    Payment,  # Subject,; Topic,
    Image,
    ResetCode,
    Transaction,
)
from api.permissions import IsInstituteOwner, ReadOnly
from api.serializers.common import *
from api.serializers.exam import *
from api.utils import get_client_country
from api.utils import clean_iamge


class ExamListView(ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = ExamSerializer

    def get_queryset(self):
        queryset = Exam.objects.all()
        user = self.request.user
        if user.is_authenticated and user.country:
            queryset = queryset.filter(countries=user.country)
        else:
            try:
                queryset = queryset.filter(countries=get_client_country(self.request))
            except:
                pass
        return queryset


# class SubjectListView(ViewSet):
#     permission_classes = (ReadOnly,)

#     def list(self, request):
#         queryset = Subject.objects.filter()
#         serializer = SubjectSerializer(queryset, many=True)
#         return Response(serializer.data)


# class TopicListView(ViewSet):
#     permission_classes = (ReadOnly,)

#     def list(self, request):
#         queryset = Topic.objects.filter()
#         serializer = TopicSerializer(queryset, many=True)
#         return Response(serializer.data)


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


class PaymentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

        processed_image = clean_iamge(uploaded_image)

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
