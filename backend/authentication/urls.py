from django.views.generic import TemplateView
from django.conf.urls import url

from .views import (
    RegisterView, RegisterStudentView ,RegisterInstituteView, VerifyEmailView, LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register-student/$', RegisterStudentView.as_view(), name='register-student'),
    url(r'^register-institute/$', RegisterInstituteView.as_view(), name='register-institute'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='verify_email'),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(), name='account_confirm_email'),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='password_change'),
]