from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from kanban_board.models import Comment, Task
from kanban_board.services.comments.entries import CommentEntry
from kanban_board.services.comments.repo import CommentsRepo



User = get_user_model()


class CommentsRepoImpl(CommentsRepo):
    def all(self, task: Task) -> QuerySet[Comment]:
        return self.qs.filter(task=task)

    def create(self, user: User, task: Task, comment_data: CommentEntry) -> Comment:
        return Comment.objects.create(
            user=user,
            task=task,
            text=comment_data.text
        )

    def update(self, comment: Comment, comment_data: CommentEntry) -> Comment:
        comment.text = comment_data.text
        comment.save()
        return comment
 
    def get_by_id(self, id: int) -> Comment:
        return self.qs.get(id=id)
