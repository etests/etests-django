from django.apps import apps
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.html import mark_safe
from django.contrib.admin.models import LogEntry
from .models import *

admin.site.register(LogEntry)

class UserTypeFilter(SimpleListFilter):
    title = "User Type"
    parameter_name = "user_type"

    def lookups(self, request, model_admin):
        return [("Staff", "Staff"), ("Institute", "Institute"), ("Student", "Student")]

    def queryset(self, request, queryset):
        if self.value() == "Staff":
            return queryset.filter(is_staff = True)
        elif self.value() == "Institute":
            return queryset.filter(is_institute = True)
        elif self.value() == "Student":
            return queryset.filter(is_student = True)
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
            return mark_safe("<a href='../institute/%d'>Institute</a>" % (obj.institute.id))
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
            return queryset.filter(student__isnull = False)
        elif self.value() == "Not Joined":
            return queryset.filter(student__isnull = True)
        else:
            return queryset.all()

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("institute", "batch", "roll_number", "joining_key", "student", "date_joined")
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
    list_filter = ("institutes", )

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ("user", "pincode", "current_credits", "verified", "show", "rating", "about")
    list_display_links = ("user",)
    list_filter = ("verified", "show", "rating", "pincode")

app_models = apps.get_app_config("authentication").get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
