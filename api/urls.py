from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    auth,
    batch,
    common,
    enrollment,
    exam,
    institute,
    password,
    question,
    session,
    test,
    testseries,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("login/", auth.LoginView.as_view()),
    path("logout/", auth.LogoutView.as_view()),
    path("register/", auth.RegisterView.as_view()),
    path("email/verify/", auth.VerifyEmailView.as_view()),
    path("email/confirm/", TemplateView.as_view()),
    path("profile/update/", auth.ProfileView.as_view()),
    path("password/request/", password.PasswordResetRequestView.as_view()),
    path("password/reset/", password.PasswordResetConfirmView.as_view()),
    path("password/change/", password.ChangePasswordView.as_view()),
    path("batches/simple/", batch.BatchListView.as_view()), #REMOVE
    path("batches/", batch.BatchListCreateView.as_view()),
    path("batch/join/<int:pk>/", batch.BatchJoinView.as_view()),
    path("batches/<int:pk>/", batch.BatchRetrieveUpdateDestoryView.as_view()),
    path("batch/enroll/", enrollment.EnrollmentView.as_view()),
    path("enrollments/", enrollment.EnrollmentView.as_view()),
    path(
        "enrollments/<int:pk>/",
        enrollment.EnrollmentRetrieveUpdateDestoryView.as_view(),
    ),
    path("institutes/joined/", institute.JoinedInstitutesView.as_view()),
    path("institutes/", institute.InstitutesListView.as_view({"get": "list"})),
    path("exams/", common.ExamListView.as_view({"get": "list"})),
    path("subjects/", common.SubjectListView.as_view({"get": "list"})),
    path("topics/", common.TopicListView.as_view({"get": "list"})),
    path(
        "tags/",
        common.TagListView.as_view(
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
    path("testseries/all/", testseries.TestSeriesListView.as_view()),
    path("testseries/", testseries.TestSeriesListCreateView.as_view()),
    path(
        "testseries/<int:pk>/", testseries.TestSeriesRetrieveUpdateDestoryView.as_view()
    ),
    path("tests/", test.TestListView.as_view()),
    path("tests/free/", test.FreeTestListView.as_view()),
    path("test/create/", test.TestCreateView.as_view()),
    path("tests/<int:pk>/", test.TestRetrieveUpdateDestoryView.as_view()),
    path("sessions/", session.SessionListView.as_view()),
    path("sessions/<int:test_id>/", session.SessionCreateRetrieveUpdateView.as_view()),
    path("generate-ranks/<int:id>/", session.GenerateRanks.as_view()),
    path("ranklist/<int:id>/", session.RankListView.as_view()),
    path("result/<int:pk>/", session.ResultView.as_view()),
    path("review/<int:pk>/", session.Review.as_view()),
    path("transactions/", common.TransactionListView.as_view()),
    path("payment/", csrf_exempt(common.PaymentView.as_view())),
    path("credit-used/", common.CreditListView.as_view()),
    path("aits-transactions/", common.AITSTransactionListView.as_view()),
    path("aits-buyers/", common.AITSBuyer.as_view()),
    path("publish-aits/", testseries.PublishTestSeries.as_view()),
    path(
        "upload-question-image/", csrf_exempt(common.UploadQuestionImageView.as_view())
    ),
    path("add-question/", question.AddQuestionAPIView.as_view()),
    path("get-questions/", question.RetrieveQuestionAPIView.as_view()),
    path(
        "evaluate-left-sessions/<int:test_id>", session.EvaluateLeftSessions.as_view()
    ),
]
