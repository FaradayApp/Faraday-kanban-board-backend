from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from kanban_board.models import Task, KanbanBoard
from kanban_board.services.tasks.entries import CreateTaskEntry
from kanban_board.services.tasks.repo import TaskRepo


User = get_user_model()


class TaskRepoImpl(TaskRepo):

    def all(self) -> QuerySet[Task]:
        return self.qs.order_by('id')
    
    def create(self, user: User, board: KanbanBoard, task_data: CreateTaskEntry) -> Task:
        return Task.objects.create(
            board=board,
            producer=user,
            title=task_data.title,
            description=task_data.description,
            expiration_date=task_data.expiration_date,
            status=task_data.status,
            priority=task_data.priority
        )

    def set_performers(self, task: Task, performers: QuerySet[User]) -> None:
        task.performers.set(performers)
