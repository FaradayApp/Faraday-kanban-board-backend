from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry
from kanban_board.services.board.repo import KanbanBoardRepo

User = get_user_model()


class CreateKanbanBoardCommand(ABC):

    @abstractmethod
    def __call__(self, board_data: CreateKanbanBoardEntry, user: User) -> KanbanBoard: ...


class CreateKanbanBoardCommandImpl(CreateKanbanBoardCommand):
    def __init__(self, repo: KanbanBoardRepo) -> None:
        self.repo = repo
    
    def __call__(self, board_data: CreateKanbanBoardEntry, user: User) -> KanbanBoard:
        board = self.repo.create(board_data=board_data)
        self.repo.add_user_to_board(board=board, user=user)
        return board
