from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry
from kanban_board.services.board.repo import KanbanBoardRepo



User = get_user_model()


class KanbanBoardRepoImpl(KanbanBoardRepo):

    def all(self) -> QuerySet[KanbanBoard]:
        return self.qs.order_by('id')
    
    def create(self, board_data: CreateKanbanBoardEntry) -> KanbanBoard:
        return KanbanBoard.objects.create(
            group_id=board_data.group_id,
        )
    
    def get_board_by_id(self, id: int) -> KanbanBoard:
        return self.qs.get(id=id)

    def add_user_to_board(self, board: KanbanBoard, user: User) -> None:
        board.users.add(user)
