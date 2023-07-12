from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from rest_framework.response import Response
from dependency_injector.wiring import Provide, inject
from users import serializers
from users import services
from drf_spectacular.utils import extend_schema

from di import Container
from users.services.repo import UserRepo
from users.services.user.create_user import CreateUserCommand
from users.services.user.login_user import LoginUserCommand
from users.services.user.tokens_service import TokensService


class RegistrationUserAPI(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

    @extend_schema(
        request=serializers.UserSerializer,
        responses={status.HTTP_201_CREATED: serializers.TokenSerializer}
    )
    def post(
            self,
            request, 
            service: CreateUserCommand = Provide[Container.create_user],
            token_service: TokensService = Provide[Container.tokens_service],
            ):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = service(user_data=serializer.to_entry())
        tokens = token_service.make_tokens(user=user)

        return Response(status=status.HTTP_201_CREATED, data=serializers.TokenSerializer(tokens).data)


class LoginUserAPI(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

    @extend_schema(
        request=serializers.LoginUserSerializer,
        responses={status.HTTP_200_OK: serializers.TokenSerializer}
    )
    def post(
            self,
            request, 
            service: LoginUserCommand = Provide[Container.login_user],
            ):
        serializer = serializers.LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = service(username=serializer.validated_data.get('username'))

        return Response(serializers.TokenSerializer(tokens).data)


class RefreshTokenAPI(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

    @extend_schema(
        request=serializers.RefreshTokenSerializer,
        responses={status.HTTP_200_OK: serializers.TokenSerializer}
    )
    def post(
            self,
            request, 
            service: LoginUserCommand = Provide[Container.login_user],
            token_service: TokensService = Provide[Container.tokens_service],
            ):
        serializer = serializers.RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = token_service.get_user_by_refresh(refresh_token=serializer.validated_data.get('refresh'))
        tokens = service(username=user.username)

        return Response(serializers.TokenSerializer(tokens).data)


class UserAPI(APIView):
    @extend_schema(
        responses={status.HTTP_200_OK: serializers.UserSerializer}
    )
    def get(
            self,
            request, 
            repo: UserRepo = Provide[Container.user_repo],
            ):
        user = repo.get_by_username(username=request.user)
        return Response(serializers.UserSerializer(user).data)
