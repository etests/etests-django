from django.views.generic import TemplateView
from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path("batches/simple/", BatchListView.as_view()),
    path("batches/", BatchListCreateView.as_view()),
    path("batch/join/", BatchJoinView.as_view()),
    path("batches/<int:pk>/", BatchRetrieveUpdateDestoryView.as_view()),
    path("batch/enroll/", EnrollmentView.as_view()),
    path("enrollments/", EnrollmentView.as_view()),
    path("enrollments/<int:pk>/", EnrollmentRetrieveUpdateDestoryView.as_view()),
    path("institutes/joined/", JoinedInstitutesView.as_view()),
    path("institutes/", InstitutesListView.as_view({"get": "list"}), name="institutes-list"),
    path("exams/", ExamListView.as_view({"get": "list"}), name="exams-list"),
    path("subjects/", SubjectListView.as_view({"get": "list"}), name="subjects-list"),
    path("topics/", TopicListView.as_view({"get": "list"}), name="topics-list"),
    path("tags/", TagListView.as_view({"get": "list", "post": "create", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="tags-list"),
    path("testseries/all/", TestSeriesListView.as_view(), name="testseries-list"),
    path("testseries/", TestSeriesListCreateView.as_view(), name="testseries-list-create"),
    path("testseries/<int:pk>/", TestSeriesRetrieveUpdateDestoryView.as_view(), name="testseries-update-delete"),
    path("tests/", TestListView.as_view(), name="test-list"),
    path("test/create/", TestCreateView.as_view(), name="test-create"),
    path("tests/<int:pk>/", TestRetrieveUpdateDestoryView.as_view(), name="test-update-delete"),
    path("get-session/<int:test_id>/", SessionRetrieveUpdateView.as_view()),
    path("update-session/<int:pk>/", SessionRetrieveUpdateView.as_view()),
    path("generate-ranks/<int:id>/", GenerateRanks.as_view()),
    path("ranklist/<int:id>/", RankListView.as_view()),
    path("result/<int:pk>/", ResultView.as_view()),
    path("review/<int:pk>/", Review.as_view()),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("payment/", csrf_exempt(PaymentView.as_view()), name="payment"),
    path("credit-used/", CreditListView.as_view(), name="credits-list"),
    path("forgot-password-request/", ResetCodeCreateView.as_view()),
    path("forgot-password-success/", ResetCodeSuccessView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("aits-transactions/",AITSTransactionListView.as_view()),
    path("aits-buyers/",AITSBuyer.as_view()),
    path("publish-aits/", PublishTestSeries.as_view()),
    path("upload-question-image/", csrf_exempt(UploadQuestionImageView.as_view())),
    path("add-question/", AddQuestionAPIView.as_view()),
    path("get-questions/", RetrieveQuestionAPIView.as_view())
]