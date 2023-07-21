import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object

from config import settings


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


class JWTSchema(OpenApiAuthenticationExtension):
    target_class = 'users.backends.JWTAuthentication'
    name = 'jwtAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix='Bearer',
            bearer_format='JWT'
        )
