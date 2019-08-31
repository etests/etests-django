from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound

from .models import *

from .app_settings import *

from .utils import jwt_encode

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

from .serializers import *


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        data = {
            'user': user,
            'token': self.token
        }
        return JWTSerializer(data).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.create(self.request.data)
        self.token = jwt_encode(user)
        return user

class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

class LoginView(GenericAPIView):
    """
    Check the credentials and return the JSONWebToken
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        print(self.serializer.validated_data)
        self.user = self.serializer.validated_data['user']
        self.token = jwt_encode(self.user)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = JWTSerializer

        data = {
            'user': self.user,
            'student': self.student,
            'institute': self.institute,
            'token': self.token
        }

        serializer = serializer_class(instance=data,
                                        context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)

        from rest_framework_jwt.settings import api_settings as jwt_settings

        if jwt_settings.JWT_AUTH_COOKIE:
            from datetime import datetime
            expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                self.token,
                                expires=expiration,
                                httponly=True)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()

class LogoutView(APIView):
    """
    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
     
        from rest_framework_jwt.settings import api_settings as jwt_settings

        if jwt_settings.JWT_AUTH_COOKIE:
            response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)

        return response

class UserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields

    Default accepted fields: name, email, phone, city, state
    Default display fields: pk, name, email, phone, city, state
    Read-only fields: pk

    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_student:
            return StudentDetailsSerializer
        if self.request.user.is_institute:
            return InstituteDetailsSerializer
        return UserDetailsSerializer

    def get_object(self):
        if self.request.user.is_student:
            return self.request.user.student
        if self.request.user.is_institute:
            return self.request.user.institute
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()

class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )

class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})