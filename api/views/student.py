from rest_framework.generics import RetrieveUpdateAPIView

from api.permissions import IsStaff
from api.models import Student
from api.permissions import IsInstituteOwner
from api.serializers.student import StudentSerializer


class StudentListView(RetrieveUpdateAPIView):
    def get_object(self):
        return self.request.user.institute

    permission_classes = (IsInstituteOwner,)
    serializer_class = StudentSerializer
