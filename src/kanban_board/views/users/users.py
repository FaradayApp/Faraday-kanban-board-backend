from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from dependency_injector.wiring import Provide, inject
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from di import Container
from kanban_board.filters import UsersInBoardFilter
from kanban_board.services.board.repo import KanbanBoardRepo
from users.serializers import UserSerializer
from utils import pagination


class UsersInBoardViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    pagination_class = pagination.DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsersInBoardFilter

    @inject
    def get_queryset(
            self,
            repo: KanbanBoardRepo = Provide[Container.board_repo],
            ):
        board = repo.get_board_by_uuid(uuid=self.kwargs.get('board_uuid'))
        repo.check_user_in_board(board=board, user=self.request.user)
        return repo.get_board_users(board=board)

    def get_serializer_class(self):
        return UserSerializer

    @extend_schema(
        responses={status.HTTP_200_OK: UserSerializer},
        description="""
            Метод для получения списка пользователей доски.
            Возвращает список пользователей, которые подключены к доске и могу работать с ней.
            В методе реализована пагинация, управлять которой можно с помощью параметров page и page_size
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
