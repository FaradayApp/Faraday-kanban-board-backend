from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from kanban_board.models import Comment, Task
from kanban_board.services.comments.entries import CommentEntry



User = get_user_model()


class CommentsRepo(ABC):
    qs = Comment.objects.all()

    @abstractmethod
    def all(self, task: Task) -> QuerySet[Comment]: ...

    @abstractmethod
    def create(self, user: User, task: Task, comment_data: CommentEntry) -> Comment: ...

    @abstractmethod
    def update(self, comment: Comment, comment_data: CommentEntry) -> Comment: ...

    @abstractmethod   
    def get_by_id(self, id: int) -> Comment: ...
