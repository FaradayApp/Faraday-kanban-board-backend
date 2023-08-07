from abc import ABC, abstractmethod
import base64
import io
import random
import string

from django.core.files import File
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
        user = self.set_avatar(user=user, avatar=user_data.avatar)
        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name
        return self.repo.save(user=user)

    def set_avatar(self, user: User, avatar: str) -> User:
        if avatar:
            allowed_chars = string.ascii_letters
            length = random.randint(15, 20)
            filename = ''.join(random.choice(allowed_chars) for _ in range(length))
            user.avatar = File(io.BytesIO(base64.b64decode(avatar)), name=filename)
        if avatar is None:
            user.avatar = None
        return user
