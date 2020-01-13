from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.html import mark_safe

from .models import *


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "_test_series",
        "institute",
        "exam",
        "activation_time",
        "closing_time",
        "_status",
    )
    list_display_links = ("name",)
    list_filter = ("free", "exam", "institute")

    def _test_series(self, obj):
        test_series = TestSeries.objects.filter(tests=obj)
        if len(test_series) > 0:
            return test_series[0].name
        else:
            return "-"

    def _status(self, obj):
        status = obj.status
        if status == 0:
            return "Inactive"
        elif status == 1:
            return "Active"
        elif status == 2:
            return "Ended"
        elif status == 3:
            return "Corrected"
        elif status == 4:
            return "Ranks Declared"


@admin.register(TestSeries)
class TestSeriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "institute", "price", "date_added", "visible")
    list_display_links = ("name",)
    list_filter = ("date_added", "exams", "institute")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "test",
        "checkin_time",
        "duration",
        "practice",
        "completed",
        "_marks",
        "_rank",
    )
    list_display_links = ("id", "student")
    list_filter = ("practice", "completed", "test")

    def _marks(self, obj):
        if obj.marks and "total" in obj.marks and "maxMarks" in obj.marks:
            return str(obj.marks["total"]) + "/" + str(obj.marks["maxMarks"][-1])

    def _rank(self, obj):
        if obj.ranks and "overall" in obj.ranks:
            return obj.ranks["overall"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "subjectIndex",
        "topicIndex",
        "difficulty",
    )
    list_display_links = ("id",)
    list_filter = ("type", "subjectIndex", "topicIndex", "difficulty")

@admin.register(ResetCode)
class ResetCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "date_added", "reset_code", "user", "done")
    list_display_links = ("reset_code",)
    list_filter = ("date_added", "done")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user",
        "test_series",
        "amount",
        "verified",
        "show",
        "receipt",
    )
    list_display_links = ("transaction_id",)
    list_filter = ("user", "test_series", "verified", "show")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "institute", "credits_added", "amount", "mode")
    list_display_links = ("transaction_id",)
    list_filter = ("institute", "mode")


app_models = apps.get_app_config("api").get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
