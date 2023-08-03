from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from kanban_board.models import Task, KanbanBoard
from kanban_board.services.tasks.entries import CreateTaskEntry, EditTaskEntry



User = get_user_model()


class TaskRepo(ABC):
    qs = Task.objects.all()

    @abstractmethod
    def all(self, board: KanbanBoard) -> QuerySet[Task]: ...

    @abstractmethod
    def create(self, user: User, board: KanbanBoard, task_data: CreateTaskEntry) -> Task: ...

    @abstractmethod
    def set_performers(self, task: Task, performers: QuerySet[User]) -> None: ...

    @abstractmethod
    def get_task_by_id(self, id: int) -> None: ...

    @abstractmethod
    def update(self, task: Task, task_data: dict) -> None: ...

    @abstractmethod
    def add_comments_count(self, qs: QuerySet[Task]) -> QuerySet[Task]: ...

    @abstractmethod
    def clear_performers(self, task: Task) -> None: ...
