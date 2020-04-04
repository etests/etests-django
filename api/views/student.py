from rest_framework.generics import ListAPIView

from api.permissions import IsStaff
from api.models import Student
from api.permissions import IsInstituteOwner
from api.serializers.student import StudentSerializer


class StudentListView(ListAPIView):
    permission_classes = (IsInstituteOwner | IsStaff,)
    serializer_class = StudentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Student.objects.all()
            elif self.request.user.is_institute:
                return self.request.user.institute.students.all()
