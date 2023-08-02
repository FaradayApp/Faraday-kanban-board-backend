from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from kanban_board.models import Comment
from kanban_board.services.comments.entries import CommentEntry
from kanban_board.services.comments.repo import CommentsRepo
from kanban_board.services.tasks.repo import TaskRepo

User = get_user_model()


class CreateCommentCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, comment_data: CommentEntry, task_id: int) -> Comment: ...


class CreateCommentCommandImpl(CreateCommentCommand):
    def __init__(self, repo: CommentsRepo, task_repo: TaskRepo) -> None:
        self.repo = repo
        self.task_repo = task_repo
    
    def __call__(self, user: User, comment_data: CommentEntry, task_id: int) -> Comment:
        task = self.task_repo.get_task_by_id(id=task_id)
        return self.repo.create(
            user=user,
            task=task,
            comment_data=comment_data
        )
