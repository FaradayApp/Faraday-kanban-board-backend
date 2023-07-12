from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random
from typing import Optional

from django.contrib.auth import get_user_model
import jwt

from config import settings
from users.services.repo import TokenRepo


User = get_user_model()


class TokensService(ABC):

    @abstractmethod
    def make_tokens(self, user: User) -> dict: ...

    @abstractmethod
    def get_user_by_refresh(self, refresh_token: str) -> Optional[User]: ...


class TokensServiceImpl(TokensService):    

    def __init__(self, repo: TokenRepo) -> None:
        self.repo = repo

    def make_tokens(self, user: User) -> dict:
        return {
            'access': self._make_access_token(user=user),
            'refresh': self._make_refresh_token(user=user)
        }
    
    def get_user_by_refresh(self, refresh_token: str) -> Optional[User]:
        return self.repo.get_user_by_refresh(refresh_token=refresh_token)

    def _make_access_token(self, user: User) -> str:
        payload = {
            'user': user.pk,
            'exp': (datetime.now() + timedelta(hours=8)).timestamp()
        }
        encoded = jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm='HS256'
        )
        return encoded


    def _make_refresh_token(self, user: User) -> str:
        payload = {
            'salt': f'{random.randbytes(16)}'
        }
        encoded = jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm='HS256'
        )
        self.repo.create_refresh_token(user=user, token=encoded)
        return encoded
    