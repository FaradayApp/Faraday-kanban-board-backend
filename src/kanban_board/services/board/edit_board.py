from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry
from kanban_board.services.board.repo import KanbanBoardRepo

User = get_user_model()


class EditKanbanBoardCommand(ABC):

    @abstractmethod
    def __call__(self, board: KanbanBoard, board_data: CreateKanbanBoardEntry) -> KanbanBoard: ...


class EditKanbanBoardCommandImpl(EditKanbanBoardCommand):
    def __init__(self, repo: KanbanBoardRepo) -> None:
        self.repo = repo
    
    def __call__(self, board: KanbanBoard, board_data: CreateKanbanBoardEntry) -> KanbanBoard:
        return self.repo.update(board=board, board_data=board_data)
    