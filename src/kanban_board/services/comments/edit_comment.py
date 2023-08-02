from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from kanban_board.models import Comment
from kanban_board.services.comments.entries import CommentEntry
from kanban_board.services.comments.repo import CommentsRepo
from kanban_board.services.tasks.repo import TaskRepo
from utils import exceptions

User = get_user_model()


class EditCommentCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, comment: Comment, comment_data: CommentEntry) -> Comment: ...


class EditCommentCommandImpl(EditCommentCommand):
    def __init__(self, repo: CommentsRepo) -> None:
        self.repo = repo
    
    def __call__(self, user: User, comment: Comment, comment_data: CommentEntry) -> Comment:
        self.validate(user=user, comment=comment)
        return self.repo.update(
            comment=comment,
            comment_data=comment_data
        )
    
    def validate(self, user: User, comment: Comment) -> None:
        if user != comment.user:
            raise exceptions.CustomException('Permission denied')
