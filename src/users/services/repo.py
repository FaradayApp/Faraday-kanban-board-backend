from abc import ABC, abstractmethod
from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from users.models import RefreshToken
from users.services.entries import UserEntry


User = get_user_model()


class UserRepo(ABC):
    qs = User.objects.all()

    @abstractmethod
    def all(self) -> QuerySet[User]: ...

    @abstractmethod
    def create(self, user_data: UserEntry) -> User: ...

    @abstractmethod
    def save(self, user: User) -> User: ...
    
    @abstractmethod
    def user_exists(self,**kwargs) -> bool: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User: ...

    @abstractmethod
    def get_users_by_ids(self, ids: List[int]) -> QuerySet[User]: ...


class TokenRepo(ABC):
    qs = RefreshToken.objects.all()

    @abstractmethod
    def create_refresh_token(self, user: User, token: str) -> None: ...
    
    @abstractmethod
    def get_user_by_refresh(self, refresh_token: str) -> Optional[User]: ...
