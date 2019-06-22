from django.views.generic import TemplateView
from django.urls import path

from .views import (
    RegisterView, RegisterStudentView ,RegisterInstituteView, VerifyEmailView, LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register/student/", RegisterStudentView.as_view(), name="register/student"),
    path("register/institute/", RegisterInstituteView.as_view(), name="register/institute"),
    path("email/verify", VerifyEmailView.as_view(), name="verify_email"),
    path("email/verify/confirm/", TemplateView.as_view(), name="confirm_email"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserDetailsView.as_view(), name="user_details"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
]