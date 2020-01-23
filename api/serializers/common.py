from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import Payment, AITSTransaction, Transaction, CreditUse, Tag, Question


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ("transaction_id", "receipt", "user", "amount", "test_series")


class AITSBuyerSerializer(ModelSerializer):
    test_series = SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("test_series", "date_added")

    def get_test_series(self, obj):
        return {"id": obj.test_series.id, "name": obj.test_series.name}


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


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


class AITSTransactionSerializer(ModelSerializer):
    test_series = SerializerMethodField()

    class Meta:
        model = AITSTransaction
        fields = "__all__"

    def get_test_series(self, obj):
        return ", ".join([test_series.name for test_series in obj.test_series.all()])


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}
