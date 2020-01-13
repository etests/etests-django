from django.views.generic import TemplateView
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email/verify", VerifyEmailView.as_view(), name="verify_email"),
    path("email/verify/confirm/", TemplateView.as_view(), name="confirm_email"),
    path("profile/update/", ProfileView.as_view(), name="profile"),
    path("forgot-password-request/", PasswordResetRequestView.as_view()),
    path("forgot-password-success/", PasswordResetConfirmView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]