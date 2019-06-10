from django.views.generic import TemplateView
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^institutes/$', InstitutesListView.as_view({'get': 'list'}), name='institutes-list'),
    
    url(r'^subjects/$', SubjectListView.as_view({'get': 'list'}), name='subjects-list'),

    url(r'^topics/$', TopicListView.as_view({'get': 'list'}), name='topics-list'),

    url(r'^tags/$', TagListView.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='tags-list'),

    url(r'^testseries/$', TestSeriesListCreateView.as_view(), name='testseries-list-create'),

    url(r'^testseries/<int:pk>/$', TestSeriesRetrieveUpdateDestoryView.as_view(), name='testseries-update-delete'),

    url(r'^tests/$', TestListCreateView.as_view(), name='test-list-create'),

    url(r'^tests/<int:pk>/$', TestRetrieveUpdateDestoryView.as_view(), name='test-update-delete'),

    url(r'^unittests/$', UnitTestListCreateView.as_view(), name='unittests-list-create'),

    url(r'^unittests/<int:pk>/$', UnitTestRetrieveUpdateDestoryView.as_view(), name='unittests-update-delete'),

    url(r'^sessions/$', SessionListView.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='sessions-list'),

    url(r'^buyers/$', BuyerListView.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='buyers-list'),
]