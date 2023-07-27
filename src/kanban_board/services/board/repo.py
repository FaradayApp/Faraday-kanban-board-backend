from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry



User = get_user_model()


class KanbanBoardRepo(ABC):
    qs = KanbanBoard.objects.all()

    @abstractmethod
    def all(self) -> QuerySet[KanbanBoard]: ...

    @abstractmethod
    def create(self, board_data: CreateKanbanBoardEntry) -> KanbanBoard: ...

    @abstractmethod   
    def get_board_by_id(self, id: int) -> KanbanBoard: ...

    @abstractmethod   
    def get_board_by_uuid(self, uuid: str) -> KanbanBoard: ...

    @abstractmethod
    def add_user_to_board(self, board: KanbanBoard, user: User) -> None: ...

    @abstractmethod
    def check_user_in_board(self, board: KanbanBoard, user: User) -> None: ...
