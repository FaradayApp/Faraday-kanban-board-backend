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


class EditTaskCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, task: Task, board_id: int, task_data: CreateTaskEntry) -> Task: ...


class EditTaskCommandImpl(EditTaskCommand):
    def __init__(self, repo: TaskRepo, user_repo: UserRepo, board_repo: KanbanBoardRepo) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.board_repo = board_repo
    
    def __call__(self, user: User, task: Task, board_id: int, task_data: CreateTaskEntry) -> Task:
        board = self.board_repo.get_board_by_id(id=board_id)
        self.validate_board(board=board, task=task)
        validated_data, performers_ids = self.validate_task_data(user=user, task=task, task_data=task_data)
        self.repo.update(task=task, task_data=validated_data)
        task = self.repo.get_task_by_id(id=task.id)
        if performers_ids:
            performers = self.user_repo.get_users_by_ids(ids=task_data.performers)
        self.repo.set_performers(task=task, performers=performers)
        return task

    def validate_task_data(self, user: User, task: Task, task_data: CreateTaskEntry) -> dict:
        is_producer = task.producer == user
        data = {}

        if task_data.performers:
            if len(task_data.performers) > 0:
                performers = task_data.performers
            else:
                performers = None
        else:
            performers = task_data.performers

        if task_data.status:
            data["status"] = task_data.status

        if is_producer:
            if task_data.title:
                data["title"] = task_data.title
            
            if task_data.expiration_date:
                data["expiration_date"] = task_data.expiration_date
            
            if task_data.priority:
                data["priority"] = task_data.priority
            
            if task_data.description:
                data["description"] = task_data.description

        return data, performers

    def validate_board(self, board: KanbanBoard, task: Task):
        if task.board != board:
            raise exceptions.CustomException('Incorrect board')
        