from abc import ABC, abstractmethod
from dataclasses import asdict

from django.contrib.auth import get_user_model

from kanban_board.models import Task, KanbanBoard
from kanban_board.services.board.repo import KanbanBoardRepo
from kanban_board.services.tasks.entries import CreateTaskEntry
from kanban_board.services.tasks.repo import TaskRepo
from users.services.repo import UserRepo
from utils import exceptions

User = get_user_model()


class DeleteTaskCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, task: Task, board_uuid: str) -> None: ...


class DeleteTaskCommandImpl(DeleteTaskCommand):
    def __init__(self, repo: TaskRepo, board_repo: KanbanBoardRepo) -> None:
        self.repo = repo
        self.board_repo = board_repo
    
    def __call__(self, user: User, task: Task, board_uuid: str) -> None:
        board = self.board_repo.get_board_by_uuid(uuid=board_uuid)
        self.validate_board(board=board, task=task)
        if task.producer == user or user.is_superuser:
            self.repo.hide(task)
        else:
            raise exceptions.CustomException('Permission denied')
            
    def validate_board(self, board: KanbanBoard, task: Task):
        if task.board != board:
            raise exceptions.CustomException('Incorrect board')
