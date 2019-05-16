from rest_framework_jwt.serializers import JSONWebTokenSerializer

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

class TokenSerializer(JSONWebTokenSerializer):
    username_field = "username"

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get(self.username_field)).first() or User.objects.filter(username=attrs.get(self.username_field)).first() or User.objects.filter(phone=attrs.get(self.username_field)).first()
        if user_obj is not None:
            credentials = {
                'username': user_obj.email,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = _('Account with these credentials does not exists')
            raise serializers.ValidationError(msg)