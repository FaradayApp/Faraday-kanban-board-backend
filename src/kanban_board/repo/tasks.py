from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.models import Count

from kanban_board.models import Task, KanbanBoard
from kanban_board.services.tasks.entries import CreateTaskEntry
from kanban_board.services.tasks.repo import TaskRepo


User = get_user_model()


class TaskRepoImpl(TaskRepo):

    def all(self, board: KanbanBoard) -> QuerySet[Task]:
        return self.qs.filter(board=board).order_by('id')
    
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
    
    def get_task_by_id(self, id: int) -> Task:
        return self.qs.get(id=id)

    def update(self, task: Task, task_data: dict) -> None:
        self.qs.filter(id=task.id).update(**task_data)
    
    def add_comments_count(self, qs: QuerySet[Task]) -> QuerySet[Task]:
        return qs.annotate(comments_count=Count('comments'))
    
    def clear_performers(self, task: Task) -> None:
        task.performers.clear()
