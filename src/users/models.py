from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from utils.models import TimestampModel
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampModel):
    username = models.CharField(
        'Username',
        unique=True,
        max_length=33,
    )
    avatar = models.ImageField("avatar", upload_to='profiles_photos/main_photos', blank=True, null=True)
    first_name = models.CharField("first name", max_length=32, blank=True, null=True)
    last_name = models.CharField("last name", max_length=32, blank=True, null=True)

    is_superuser = models.BooleanField("superuser", default=False)
    is_staff = models.BooleanField("staff", default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=256, unique=True)
    expire_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
