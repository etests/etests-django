from django.conf import settings

from .serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
    JWTSerializer as DefaultJWTSerializer,
    UserDetailsSerializer as DefaultUserDetailsSerializer,
    LoginSerializer as DefaultLoginSerializer,
    PasswordResetSerializer as DefaultPasswordResetSerializer,
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
    PasswordChangeSerializer as DefaultPasswordChangeSerializer)

from .utils import import_callable

from rest_framework.permissions import AllowAny

serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})

RegisterSerializer = import_callable(
    serializers.get('REGISTER_SERIALIZER', DefaultRegisterSerializer))

def register_permission_classes():
    permission_classes = [AllowAny, ]
    for permission_class in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(permission_class))
    return tuple(permission_classes)


serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

JWTSerializer = import_callable(
    serializers.get('JWT_SERIALIZER', DefaultJWTSerializer))

UserDetailsSerializer = import_callable(
    serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)

PasswordResetSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_SERIALIZER',
        DefaultPasswordResetSerializer
    )
)

PasswordResetConfirmSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_CONFIRM_SERIALIZER',
        DefaultPasswordResetConfirmSerializer
    )
)

PasswordChangeSerializer = import_callable(
    serializers.get(
        'PASSWORD_CHANGE_SERIALIZER',
        DefaultPasswordChangeSerializer
    )
)