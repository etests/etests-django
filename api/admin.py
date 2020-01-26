from django.apps import apps
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.html import mark_safe

from .models import *

admin.site.register(LogEntry)


class UserTypeFilter(SimpleListFilter):
    title = "User Type"
    parameter_name = "user_type"

    def lookups(self, request, model_admin):
        return [("Staff", "Staff"), ("Institute", "Institute"), ("Student", "Student")]

    def queryset(self, request, queryset):
        if self.value() == "Staff":
            return queryset.filter(is_staff=True)
        elif self.value() == "Institute":
            return queryset.filter(is_institute=True)
        elif self.value() == "Student":
            return queryset.filter(is_student=True)
        else:
            return queryset.all()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "user_type")
    list_display_links = ("name",)
    list_filter = (UserTypeFilter,)

    def user_type(self, obj):
        if obj.is_student:
            return mark_safe("<a href='../student/%d'>Student</a>" % (obj.student.id))
        elif obj.is_institute:
            return mark_safe(
                "<a href='../institute/%d'>Institute</a>" % (obj.institute.id)
            )
        elif obj.is_staff:
            return "Staff"
        else:
            return "User"


class EnrollmentStatusFilter(SimpleListFilter):
    title = "Enrollment Status"
    parameter_name = "enroll_status"

    def lookups(self, request, model_admin):
        return [("Joined", "Joined"), ("Not Joined", "Not Joined")]

    def queryset(self, request, queryset):
        if self.value() == "Joined":
            return queryset.filter(student__isnull=False)
        elif self.value() == "Not Joined":
            return queryset.filter(student__isnull=True)
        else:
            return queryset.all()


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "institute",
        "batch",
        "roll_number",
        "joining_key",
        "student",
        "date_joined",
    )
    list_display_links = ("roll_number",)
    list_filter = (EnrollmentStatusFilter, "institute")


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("institute", "name")
    list_display_links = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "birth_date")
    list_display_links = ("user",)
    list_filter = ("institutes",)


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pincode",
        "current_credits",
        "verified",
        "show",
        "rating",
        "about",
    )
    list_display_links = ("user",)
    list_filter = ("verified", "show", "rating", "pincode")

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
        if obj.marks and "total" in obj.marks and "max_marks" in obj.marks:
            return str(obj.marks["total"]) + "/" + str(obj.marks["max_marks"][-1])

    def _rank(self, obj):
        if obj.ranks and "overall" in obj.ranks:
            return obj.ranks["overall"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "subjectIndex", "topicIndex", "difficulty")
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
