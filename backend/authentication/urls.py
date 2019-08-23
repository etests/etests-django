from django.views.generic import TemplateView
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from .views import (
    RegisterView, VerifyEmailView, LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email/verify", VerifyEmailView.as_view(), name="verify_email"),
    path("email/verify/confirm/", TemplateView.as_view(), name="confirm_email"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", refresh_jwt_token),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserDetailsView.as_view(), name="user_details"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
]