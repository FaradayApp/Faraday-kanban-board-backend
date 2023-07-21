from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from kanban_board.models import Task, KanbanBoard
from kanban_board.services.board.repo import KanbanBoardRepo
from kanban_board.services.tasks.entries import CreateTaskEntry
from kanban_board.services.tasks.repo import TaskRepo
from users.services.repo import UserRepo

User = get_user_model()


class CreateTaskCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, board_id: int, task_data: CreateTaskEntry) -> Task: ...


class CreateTaskCommandImpl(CreateTaskCommand):
    def __init__(self, repo: TaskRepo, user_repo: UserRepo, board_repo: KanbanBoardRepo) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.board_repo = board_repo
    
    def __call__(self, user: User, board_id: int, task_data: CreateTaskEntry) -> Task:
        board = self.board_repo.get_board_by_id(id=board_id)
        task = self.repo.create(user=user, board=board, task_data=task_data)
        performers = self.user_repo.get_users_by_ids(ids=task_data.performers)
        self.repo.set_performers(task=task, performers=performers)
        return task
