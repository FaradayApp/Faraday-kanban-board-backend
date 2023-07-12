from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from users.services.repo import UserRepo
from users.services.user.tokens_service import TokensService
from utils import exceptions


User = get_user_model()


class LoginUserCommand(ABC):

    @abstractmethod
    def __call__(self, username: str) -> User: ...


class LoginUserCommandImpl(LoginUserCommand):
    def __init__(self, repo: UserRepo, tokens_service: TokensService) -> None:
        self.repo = repo
        self.tokens_service = tokens_service
    
    def __call__(self, username: str) -> User:
        if self.repo.user_exists(username=username):
            user = self.repo.get_by_username(username=username)
            return self.tokens_service.make_tokens(user=user)
        else:
            raise exceptions.CustomException('User is not found')
