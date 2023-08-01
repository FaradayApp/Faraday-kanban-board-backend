from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from kanban_board.services.board.repo import KanbanBoardRepo


User = get_user_model()


class AddUserToBoardCommand(ABC):

    @abstractmethod
    def __call__(self, user: User, board_uuid: str) -> None: ...


class AddUserToBoardCommandImpl(AddUserToBoardCommand):
    def __init__(self, repo: KanbanBoardRepo) -> None:
        self.repo = repo
    
    def __call__(self, user: User, board_uuid: str) -> None:
        board = self.repo.get_board_by_uuid(uuid=board_uuid)
        self.repo.add_user_to_board(board=board, user=user)

