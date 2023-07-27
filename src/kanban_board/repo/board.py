import uuid

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry
from kanban_board.services.board.repo import KanbanBoardRepo
from utils import exceptions



User = get_user_model()


class KanbanBoardRepoImpl(KanbanBoardRepo):

    def all(self) -> QuerySet[KanbanBoard]:
        return self.qs.order_by('id')
    
    def create(self, board_data: CreateKanbanBoardEntry) -> KanbanBoard:
        return KanbanBoard.objects.create(
            title=board_data.title,
            uuid=str(uuid.uuid4())
        )    
    
    def update(self, board: KanbanBoard, board_data: CreateKanbanBoardEntry) -> KanbanBoard:
        board.title = board_data.title
        board.save()
        return board
    
    def get_board_by_id(self, id: int) -> KanbanBoard:
        return self.qs.get(id=id)

    def get_board_by_uuid(self, uuid: str) -> KanbanBoard:
        return self.qs.get(uuid=uuid)

    def add_user_to_board(self, board: KanbanBoard, user: User) -> None:
        board.users.add(user)
    
    def check_user_in_board(self, board: KanbanBoard, user: User) -> None:
        if not user in board.users.all():
            raise exceptions.CustomException('Permissions denied')
