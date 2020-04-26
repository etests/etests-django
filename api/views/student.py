from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView

from api.permissions import IsStaff
from api.models import Student
from api.permissions import IsInstituteOwner
from api.serializers.student import StudentSerializer, JoiningKeySerializer
from rest_framework.response import Response
from rest_framework import status


class StudentListView(ListAPIView):
    permission_classes = (IsInstituteOwner | IsStaff,)
    serializer_class = StudentSerializer

    def get_queryset(self):
        students = []
        if self.request.user.is_staff:
            students = Student.objects.all()
        elif self.request.user.is_institute:
            students = (
                Student.objects.filter(institutes=self.request.user.institute)
                .prefetch_related("user")
                .all()
            )
        return [student.user for student in students]


class StudentDeleteView(GenericAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = StudentSerializer

    def delete(self, request, pk):
        request.user.institute.students.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class JoiningKeyView(RetrieveUpdateAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = JoiningKeySerializer

    def get_object(self):
        return self.request.user.institute
