from dependency_injector import containers, providers

from kanban_board.repo.board import KanbanBoardRepoImpl
from kanban_board.repo.comments import CommentsRepoImpl
from kanban_board.repo.tasks import TaskRepoImpl
from kanban_board.services.board.create_board import CreateKanbanBoardCommandImpl
from kanban_board.services.board.edit_board import EditKanbanBoardCommandImpl
from kanban_board.services.comments.create_comment import CreateCommentCommandImpl
from kanban_board.services.comments.edit_comment import EditCommentCommandImpl
from kanban_board.services.tasks.create_task import CreateTaskCommandImpl
from kanban_board.services.tasks.edit_task import EditTaskCommandImpl

from users.repo.token import TokenRepoImpl
from users.repo.user import UserRepoImpl
from users.services.user.create_user import CreateUserCommandImpl
from users.services.user.edit_user import EditUserCommandImpl
from users.services.user.login_user import LoginUserCommandImpl
from users.services.user.tokens_service import TokensServiceImpl


class Container(containers.DeclarativeContainer):
    # users
    user_repo = providers.Singleton(UserRepoImpl)
    token_repo = providers.Singleton(TokenRepoImpl)

    create_user = providers.Singleton(
        CreateUserCommandImpl,
        repo=user_repo
    )
    edit_user = providers.Singleton(
        EditUserCommandImpl,
        repo=user_repo
    )
    tokens_service = providers.Singleton(
        TokensServiceImpl,
        repo=token_repo
    )
    login_user = providers.Singleton(
        LoginUserCommandImpl,
        repo=user_repo,
        tokens_service=tokens_service
    )

    # board
    board_repo = providers.Singleton(KanbanBoardRepoImpl)
    task_repo = providers.Singleton(TaskRepoImpl)

    create_board = providers.Singleton(
        CreateKanbanBoardCommandImpl,
        repo=board_repo
    )
    edit_board = providers.Singleton(
        EditKanbanBoardCommandImpl,
        repo=board_repo
    )
    create_task = providers.Singleton(
        CreateTaskCommandImpl,
        repo=task_repo,
        user_repo=user_repo,
        board_repo=board_repo
    )
    edit_task = providers.Singleton(
        EditTaskCommandImpl,
        repo=task_repo,
        user_repo=user_repo,
        board_repo=board_repo
    )

    #comments
    comments_repo =  providers.Singleton(CommentsRepoImpl)

    create_comment = providers.Singleton(
        CreateCommentCommandImpl,
        repo=comments_repo,
        task_repo=task_repo
    )
    edit_comment = providers.Singleton(
        EditCommentCommandImpl,
        repo=comments_repo
    )

