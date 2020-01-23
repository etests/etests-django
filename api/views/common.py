from io import BytesIO

import cv2
import numpy as np
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.forms import PaymentForm, QuestionImageUploadForm
from api.models import (
    AITSTransaction,
    Exam,
    Payment,
    QuestionImage,
    ResetCode,
    Subject,
    Tag,
    Topic,
    Transaction,
)
from api.permissions import IsInstituteOwner, ReadOnly
from api.serializers.common import *
from api.serializers.exam import *
from ml.preprocessing import clean


class ExamListView(ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Exam.objects.filter()
        serializer = ExamListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class SubjectListView(ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Subject.objects.filter()
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)


class TopicListView(ViewSet):
    permission_classes = (ReadOnly,)

    def list(self, request):
        queryset = Topic.objects.filter()
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data)


class TagListView(ModelViewSet):
    permission_classes = (ReadOnly | IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TransactionListView(ListAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Transaction.objects.filter(institute=self.request.user.institute)
        return None


class AITSTransactionListView(ListAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = AITSTransactionSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return AITSTransaction.objects.filter(institute=self.request.user.institute)
        return None


class CreditListView(ListAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = CreditUseSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return CreditUse.objects.filter(institute=self.request.user.institute)
        return None


class PaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            send_mail(
                payment.user.email,
                "Payment Verification in Progress",
                f"Your payment of Rs. {str(payment.test_series.price)} for {payment.test_series.name}  will be verified shortly. The AITS will appear on your dashboard after payment is verified. If you have any query feel free to email us at help@etests.co.in",
            )
            return Response("Successful", status=status.HTTP_201_CREATED)
        else:
            raise ParseError("Invalid")


class AITSBuyer(ListAPIView):
    permission_classes = (ReadOnly, IsAuthenticated)
    serializer_class = AITSBuyerSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Payment.objects.filter(
                test_series__institute=self.request.user.institute,
                verified=True,
                show=True,
            )
        elif self.request.user.is_staff:
            return Payment.objects.filter(verified=True, show=True)
        else:
            return None


class UploadQuestionImageView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        uploaded_image = request.FILES.get("upload")
        raw_image = cv2.imdecode(
            np.fromstring(uploaded_image.read(), np.uint8), cv2.IMREAD_UNCHANGED
        )
        cleaned_image = clean(raw_image)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        _, image_buffer = cv2.imencode(".jpg", cleaned_image, encode_param)

        processed_image = SimpleUploadedFile(
            "question.jpg", BytesIO(image_buffer).getvalue()
        )

        if processed_image.size < uploaded_image.size:
            request.FILES["file"] = processed_image
        else:
            request.FILES["file"] = uploaded_image

        form = QuestionImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return JsonResponse(
                {"uploaded": 1, "fileName": image.file.name, "url": image.file.url}
            )
        else:
            return JsonResponse(
                {"uploaded": 0, "error": {"message": form.errors.as_text()}}
            )
