from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import *

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("name", "_test_series", "institute", "exam", "activation_time", "closing_time")
    list_display_links = ("name",)
    list_filter = ("institute", "free", "exam")

    def _test_series(self, obj):
        test_series = TestSeries.objects.filter(tests = obj)
        if len(test_series) >0 :
            return test_series[0].name 
        else:
            return "-"


app_models = apps.get_app_config('api').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass