from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model, authenticate

from users.services.repo import UserRepo
from users.services.user.tokens_service import TokensService
from utils import exceptions


User = get_user_model()


class LoginUserCommand(ABC):

    @abstractmethod
    def __call__(self, username: str, password: str) -> dict: ...

    @abstractmethod
    def login_admin_user(self, username: str, password: str) -> dict: ...


class LoginUserCommandImpl(LoginUserCommand):
    def __init__(self, repo: UserRepo, tokens_service: TokensService) -> None:
        self.repo = repo
        self.tokens_service = tokens_service
    
    def __call__(self, username: str, password: str) -> dict:
        if self.repo.user_exists(username=username):
            user = authenticate(username=username, password=password)
            if user.is_superuser:
                self.__raise_user_not_found()
            return self.tokens_service.make_tokens(user=user)
        else:
            self.__raise_user_not_found()
    
    def login_admin_user(self, username: str, password: str) -> dict:
        if self.repo.user_exists(username=username):
            user = authenticate(username=username, password=password)
            if not user:
                raise exceptions.CustomException('Wrong login or password')
            if not user.is_superuser:
                self.__raise_user_not_found()
            return self.tokens_service.make_tokens(user=user)
        else:
            self.__raise_user_not_found()

    def __raise_user_not_found(self):
        raise exceptions.Custom404Exception('User is not found')
