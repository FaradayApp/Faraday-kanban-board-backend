from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from users.services.entries import UserEntry


User = get_user_model()


class UserRepo(ABC):
    qs = User.objects.all()

    @abstractmethod
    def all(self) -> QuerySet[User]: ...

    @abstractmethod
    def create(self, user_data: UserEntry) -> User: ...
