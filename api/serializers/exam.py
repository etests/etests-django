from rest_framework.serializers import ModelSerializer, StringRelatedField

from api.models import Exam

class ExamSerializer(ModelSerializer):
    countries = StringRelatedField(many=True)
    class Meta:
        model = Exam
        fields = ("id", "name", "start_date", "test_series", "image", "position", "countries")
