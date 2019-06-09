from django.views.generic import TemplateView
from django.conf.urls import url
from .views import InstitutesListView

urlpatterns = [
    url(r'^institutes/$', InstitutesListView.as_view({'get': 'list'}), name='institutes-list'),
]