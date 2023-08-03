from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from users.services.entries import EditUserEntry
from users.services.repo import UserRepo


User = get_user_model()


class EditUserCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, user_data: EditUserEntry) -> User: ...


class EditUserCommandImpl(EditUserCommand):
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo
    
    def __call__(self, user: User, user_data: EditUserEntry) -> User:
        if user_data.avatar:
            user.avatar = user_data.avatar
        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name
        return self.repo.save(user=user)
