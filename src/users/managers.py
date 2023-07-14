import random
import string
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_password(self.generate_random_password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(username, password, **extra_fields)
        user.save()
        return user
    
    def generate_random_password(self) -> str:
        length = random.randint(15, 20)
        allowed_chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(allowed_chars) for _ in range(length))
