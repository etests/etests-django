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
    path("batches/simple/", batch.BatchListView.as_view()),
    path("batches/", batch.BatchListCreateView.as_view()),
    path("batches/<int:pk>/enrollments/", batch.BatchJoinView.as_view()),
    path("batches/<int:pk>/", batch.BatchRetrieveUpdateDestoryView.as_view()),
    path("credits/", common.CreditListView.as_view()),
    path("enrollments/", enrollment.EnrollmentView.as_view()),
    path(
        "enrollments/<int:pk>/",
        enrollment.EnrollmentRetrieveUpdateDestoryView.as_view(),
    ),
    path("images/", csrf_exempt(common.UploadQuestionImageView.as_view())),
    path("institutes/joined/", institute.JoinedInstitutesView.as_view()),
    path("institutes/", institute.InstitutesListView.as_view()),
    path("exams/", common.ExamListView.as_view({"get": "list"})),
    # path("subjects/", common.SubjectListView.as_view({"get": "list"})),
    # path("topics/", common.TopicListView.as_view({"get": "list"})),
    path("testseries/", testseries.TestSeriesListView.as_view()),
    path("user/testseries/", testseries.TestSeriesListCreateView.as_view()),
    path(
        "testseries/<int:pk>/", testseries.TestSeriesRetrieveUpdateDestoryView.as_view()
    ),
    path("tests/", test.TestListCreateView.as_view()),
    path("tests/free/", test.FreeTestListView.as_view()),
    path("tests/<int:pk>/", test.TestRetrieveUpdateDestoryView.as_view()),
    path("tests/<int:test_id>/sessions/", session.SessionCreateRetrieveView.as_view()),
    path("sessions/", session.SessionListView.as_view()),
    path("sessions/<int:pk>/", session.SessionUpdateView.as_view()),
    path("ranks/<int:id>/", session.RankListView.as_view()),
    path("results/<int:pk>/", session.ResultView.as_view()),
    path("transactions/", common.TransactionListView.as_view()),
    path("payments/", csrf_exempt(common.PaymentView.as_view())),
    path("testseries/transactions/", common.TestSeriesTransactionListView.as_view()),
    path("testseries/buyers/", common.TestSeriesBuyersView.as_view()),
    path("questions/", question.AddQuestionAPIView.as_view()),
    path("questions/", question.RetrieveQuestionAPIView.as_view()),
]
