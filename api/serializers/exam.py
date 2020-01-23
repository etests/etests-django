from rest_framework.serializers import ModelSerializer

from api.models import Exam

class ExamSerializer(ModelSerializer):
    class Meta:
        model = Exam
        fields = ("id", "name", "start_date", "test_series", "image", "position")
