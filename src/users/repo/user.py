from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from users.services.entries import UserEntry

from users.services.repo import UserRepo

User = get_user_model()


class UserRepoImpl(UserRepo):

    def all(self) -> QuerySet[User]:
        return self.qs.order_by('id')
    
    def create(self, user_data: UserEntry) -> User:
        return User.objects.create(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            avatar=user_data.avatar
        )
