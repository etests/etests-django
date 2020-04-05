from django.conf.urls import include, url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    auth,
    common,
    institute,
    password,
    question,
    session,
    student,
    test,
    testseries,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("login/", auth.LoginView.as_view()),
    path("logout/", auth.LogoutView.as_view()),
    path("register/", auth.RegisterView.as_view()),
    # path("login/social/", auth.SocialLoginView.as_view()),
    path("email/verify/", auth.VerifyEmailView.as_view()),
    path("email/confirm/", TemplateView.as_view()),
    path("profile/", auth.ProfileView.as_view()),
    path("password/request/", password.PasswordResetRequestView.as_view()),
    path("password/reset/", password.PasswordResetConfirmView.as_view()),
    path("password/change/", password.ChangePasswordView.as_view()),
    path("credits/", common.CreditListView.as_view()),
    path("images/", csrf_exempt(common.UploadImageView.as_view())),
    path("institutes/", institute.InstitutesListView.as_view()),
    path("institutes/joined/", institute.JoinedInstitutesView.as_view()),
    path("institutes/<str:handle>/", institute.InstitutesView.as_view()),
    path("contacts/", institute.ContactView.as_view()),
    path("exams/", common.ExamListView.as_view()),
    path("payments/gateway/", common.PaymentGatewayView.as_view()),
    path("payments/<str:transaction_id>/", common.PaymentView.as_view()),
    path("questions/", question.QuestionView.as_view()),
    path("questions/<int:pk>/", question.QuestionUpdateView.as_view()),
    path("students/", student.StudentListView.as_view()),
    path("tests/", test.TestListCreateView.as_view()),
    path("tests/free/", test.FreeTestListView.as_view()),
    path("tests/<int:pk>/", test.TestRetrieveUpdateDestoryView.as_view()),
    path("tests/<int:test_id>/sessions/", session.SessionCreateRetrieveView.as_view()),
    path("ranks/<int:id>/", session.RankListView.as_view()),
    path("results/<int:pk>/", session.ResultView.as_view()),
    path("sessions/", session.SessionListView.as_view()),
    path("sessions/<int:pk>/", session.SessionUpdateView.as_view()),
    path("subjects/", common.SubjectListView.as_view()),
    path("testseries/", testseries.TestSeriesListView.as_view()),
    path("testseries/<int:pk>/", testseries.TestSeriesRetrieveView.as_view()),
    path("testseries/user/", testseries.TestSeriesListCreateView.as_view()),
    path(
        "testseries/user/<int:pk>/",
        testseries.TestSeriesRetrieveUpdateDestoryView.as_view(),
    ),
    path("testseries/transactions/", common.TestSeriesTransactionListView.as_view()),
    path("testseries/buyers/", common.TestSeriesBuyersView.as_view()),
    path("transactions/", common.TransactionListView.as_view()),
]
