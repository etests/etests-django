from django.views.generic import TemplateView
from django.conf.urls import url
from django.urls import include, path
from .views import *

urlpatterns = [
    path("batches/simple/", BatchListView.as_view()),

    path("batches/", BatchListCreateView.as_view()),

    path("batch/join/", BatchJoinView.as_view()),

    path("batches/<int:pk>/", BatchRetrieveUpdateDestoryView.as_view()),

    path("batch/enroll/", EnrollmentView.as_view()),

    path("enrollments/", EnrollmentView.as_view()),

    path("enrollments/<int:pk>/", EnrollmentRetrieveUpdateDestoryView.as_view()),

    path("institute/join/<int:pk>/", InstituteJoinView.as_view()),

    path("institutes/", InstitutesListView.as_view({"get": "list"}), name="institutes-list"),
    
    path("subjects/", SubjectListView.as_view({"get": "list"}), name="subjects-list"),

    path("topics/", TopicListView.as_view({"get": "list"}), name="topics-list"),

    path("tags/", TagListView.as_view({"get": "list", "post": "create", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="tags-list"),

    path("testseries/", TestSeriesListCreateView.as_view(), name="testseries-list-create"),

    path("testseries/<int:pk>/", TestSeriesRetrieveUpdateDestoryView.as_view(), name="testseries-update-delete"),

    path("tests/", TestListView.as_view(), name="test-list"),

    path("create-test/", TestCreateView.as_view()),

    path("tests/<int:pk>/", TestRetrieveUpdateDestoryView.as_view(), name="test-update-delete"),

    path("get-session/<int:test_id>/", SessionRetrieveUpdateView.as_view()),

    path("update-session/<int:pk>/", SessionRetrieveUpdateView.as_view()),

    path("result/<int:pk>/", ResultView.as_view()),

    path("review/<int:pk>/", Review.as_view()),

    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("credit-used/", CreditListView.as_view(), name="credits-list")
]