from api.serializers.test import *
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api.permissions import *
from api.models import Test, Batch, Exam


class TestListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["institute"]

    def get_serializer_class(self):
        if self.request.user.is_student:
            return StudentTestListSerializer
        else:
            return TestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(
                    aits=False, institute=self.request.user.institute
                )
            elif self.request.user.is_student:
                return Test.objects.filter(
                    aits=False,
                    registered_students=self.request.user.student,
                    visible=True,
                )
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None


class FreeTestListView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return StudentTestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
            return Test.objects.filter(
                free=True, sessions__student=self.request.user.student, visible=True
            ).distinct()
        else:
            return None


class TestCreateView(CreateAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = TestCreateSerializer

    def perform_create(self, serializer):
        test_series_ids = self.request.data.pop("test_series", None)
        exam_id = self.request.data.get("exam", None)
        free = self.request.data.get("free", False)
        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
                for test_series_id in test_series_ids:
                    try:
                        test_series = TestSeries.objects.get(id=test_series_id)
                        test_series.exams.add(exam)
                        if test_series.price == 0:
                            free = True
                    except:
                        pass
            except Exception as e:
                pass
        batches = self.request.data.pop("batches", None)
        student_ids = []
        if batches:
            for batch_id in batches:
                try:
                    batch = Batch.objects.get(id=batch_id)
                    if batch.institute == self.request.user.institute:
                        student_ids += [student.id for student in batch.students()]
                except Exception as e:
                    pass
        serializer.save(
            institute=self.request.user.institute,
            registered_students=student_ids,
            free=free,
        )


class TestRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | IsAdminUser,)
    serializer_class = TestSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None

