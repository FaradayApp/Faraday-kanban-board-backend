import jwt
from rest_framework import authentication, exceptions

from config import settings
from django.contrib.auth import get_user_model


User = get_user_model()


def authenticate_credentials(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.PyJWTError:
        raise exceptions.AuthenticationFailed('Token is not correct')

    try:
        user = User.objects.get(id=payload['user'])
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('Token is not correct')

    User.objects.filter(id=user.pk)

    return user, token


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or not len(auth_header) == 2:
            return None

        prefix = auth_header[0].decode()
        token = auth_header[1].decode()

        if prefix.lower() != auth_header_prefix:
            return None

        user, token = authenticate_credentials(token)
        return user, token
