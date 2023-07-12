from datetime import timedelta
from typing import Optional
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from users.models import RefreshToken

from users.services.repo import TokenRepo


User = get_user_model()


class TokenRepoImpl(TokenRepo):
    def create_refresh_token(self, user: User, token: str) -> None:
        RefreshToken.objects.create(
            user=user,
            token=token,
            expire_at=timezone.now() + timedelta(days=30)
        )

    def get_user_by_refresh(self, refresh_token: str) -> Optional[User]:
        return get_object_or_404(
            User,
            refresh_tokens__token=refresh_token,
            refresh_tokens__is_active=True
        )
