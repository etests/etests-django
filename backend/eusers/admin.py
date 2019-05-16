from django.contrib import admin
from django.db import models, migrations
from .models import *

class UserModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "state", "city"]
    list_display_links = ["email"]
    list_filter = ["state","city"]
    search_fields = ["name", "email"]
    class Meta:
        model = User

admin.site.register(User, UserModelAdmin)

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ["user", "birth_date", "institute"]
    list_filter = ["gender", "institute"]
    search_fields = [ "user", "institute"]
    class Meta:
        model = Student

admin.site.register(Student, StudentModelAdmin)

class InstituteModelAdmin(admin.ModelAdmin):
    list_display = ["user", "pincode"]
    list_filter = ["pincode"]
    search_fields = ["user", "pincode"]
    class Meta:
        list_filter = ["gender", "institute"]
        model = Institute

admin.site.register(Institute, InstituteModelAdmin)
