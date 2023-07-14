from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from users.services.entries import UserEntry
from users.services.repo import UserRepo


User = get_user_model()


class CreateUserCommand(ABC):

    @abstractmethod
    def __call__(self, user_data: UserEntry) -> User: ...


class CreateUserCommandImpl(CreateUserCommand):
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo
    
    def __call__(self, user_data: UserEntry) -> User:
        return self.repo.create(user_data=user_data)
