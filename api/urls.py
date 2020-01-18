from django.views.generic import TemplateView
from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from .views import *
from django.views.generic import TemplateView
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("register/", RegisterView.as_view()),
    path("email/verify", VerifyEmailView.as_view()),
    path("email/verify/confirm/", TemplateView.as_view()),
    path("profile/update/", ProfileView.as_view()),
    path("forgot-password-request/", PasswordResetRequestView.as_view()),
    path("forgot-password-success/", PasswordResetConfirmView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("batches/simple/", BatchListView.as_view()),
    path("batches/", BatchListCreateView.as_view()),
    path("batch/join/<int:pk>/", BatchJoinView.as_view()),
    path("batches/<int:pk>/", BatchRetrieveUpdateDestoryView.as_view()),
    path("batch/enroll/", EnrollmentView.as_view()),
    path("enrollments/", EnrollmentView.as_view()),
    path("enrollments/<int:pk>/", EnrollmentRetrieveUpdateDestoryView.as_view()),
    path("institutes/joined/", JoinedInstitutesView.as_view()),
    path("institutes/", InstitutesListView.as_view({"get": "list"})),
    path("exams/", ExamListView.as_view({"get": "list"})),
    path("subjects/", SubjectListView.as_view({"get": "list"})),
    path("topics/", TopicListView.as_view({"get": "list"})),
    path(
        "tags/",
        TagListView.as_view(
            {
                "get": "list",
                "post": "create",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="tags-list",
    ),
    path("testseries/all/", TestSeriesListView.as_view()),
    path("testseries/", TestSeriesListCreateView.as_view()),
    path("testseries/<int:pk>/", TestSeriesRetrieveUpdateDestoryView.as_view()),
    path("tests/", TestListView.as_view()),
    path("tests/free/", FreeTestListView.as_view()),
    path("test/create/", TestCreateView.as_view()),
    path("tests/<int:pk>/", TestRetrieveUpdateDestoryView.as_view()),
    path("sessions/", SessionListView.as_view()),
    path("sessions/<int:test_id>/", SessionCreateUpdateView.as_view()),
    path("generate-ranks/<int:id>/", GenerateRanks.as_view()),
    path("ranklist/<int:id>/", RankListView.as_view()),
    path("result/<int:pk>/", ResultView.as_view()),
    path("review/<int:pk>/", Review.as_view()),
    path("transactions/", TransactionListView.as_view()),
    path("payment/", csrf_exempt(PaymentView.as_view())),
    path("credit-used/", CreditListView.as_view()),
    path("aits-transactions/", AITSTransactionListView.as_view()),
    path("aits-buyers/", AITSBuyer.as_view()),
    path("publish-aits/", PublishTestSeries.as_view()),
    path("upload-question-image/", csrf_exempt(UploadQuestionImageView.as_view())),
    path("add-question/", AddQuestionAPIView.as_view()),
    path("get-questions/", RetrieveQuestionAPIView.as_view()),
    path("evaluate-left-sessions/<int:test_id>", EvaluateLeftSessions.as_view()),
]

