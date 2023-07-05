from dependency_injector import containers, providers

from users.repo.user import UserRepoImpl
from users.services.user.create_user import CreateUserCommandImpl


class Container(containers.DeclarativeContainer):
    # users
    user_repo = providers.Singleton(UserRepoImpl)

    create_user = providers.Singleton(
        CreateUserCommandImpl,
        repo=user_repo
    )
