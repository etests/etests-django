from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError
)
from api.models import Payment, AITSTransaction, Transaction, CreditUse, Tag, Question


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ("transaction_id", "receipt", "user", "amount", "test_series")

    def validate_test_series(self, test_series):
        if Payment.objects.filter(user=self.context.get("request").user, test_series=test_series):
            raise ValidationError("You have already made a payment")
        return test_series


class PaymentListSerializer(ModelSerializer):
    test_series = SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("test_series", "date_added")

    def get_test_series(self, obj):
        return {"id": obj.test_series.id, "name": obj.test_series.name}


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CreditUseSerializer(ModelSerializer):
    test = SerializerMethodField("get_test_name")

    class Meta:
        model = CreditUse
        fields = "__all__"

    def get_test_name(self, obj):
        return obj.test.name


class TestSeriesTransactionSerializer(ModelSerializer):
    test_series = StringRelatedField(many=True)

    class Meta:
        model = AITSTransaction
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}
