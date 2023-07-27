from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from rest_framework.response import Response
from dependency_injector.wiring import Provide, inject
from drf_spectacular.utils import extend_schema

from di import Container
from kanban_board.serializers.board import CreateKanbanBoardSerializer, KanbanBoardPreviewSerializer
from kanban_board.services.board.create_board import CreateKanbanBoardCommand
from kanban_board.services.board.edit_board import EditKanbanBoardCommand
from kanban_board.services.board.repo import KanbanBoardRepo
from utils import pagination
from utils.mixins import CustomCreateModelMixin, CustomUpdateModelMixin


class KanbanBoardViewSet(
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):  
    permission_classes = (IsAdminUser,)
    pagination_class = pagination.DefaultPagination

    @inject
    def get_queryset(
            self,
            repo: KanbanBoardRepo = Provide[Container.board_repo],
            ):
        return repo.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CreateKanbanBoardSerializer
        return KanbanBoardPreviewSerializer

    @extend_schema(
        request=CreateKanbanBoardSerializer,
        responses={status.HTTP_201_CREATED: KanbanBoardPreviewSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @inject
    def perform_create(
        self,
        serializer: CreateKanbanBoardSerializer,
        service: CreateKanbanBoardCommand = Provide[Container.create_board],
    ):
        board = service(
            board_data=serializer.to_entry(),
            user=self.request.user
            )

        return KanbanBoardPreviewSerializer(board, many=False, context={'request': self.request})

    @extend_schema(
        request=CreateKanbanBoardSerializer,
        responses={status.HTTP_200_OK: KanbanBoardPreviewSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @inject
    def perform_update(
        self,
        serializer: CreateKanbanBoardSerializer,
        service: EditKanbanBoardCommand = Provide[Container.edit_board]
    ):
        board = service(
            board=serializer.instance,
            board_data=serializer.to_entry(),
            )

        return KanbanBoardPreviewSerializer(board, many=False, context={'request': self.request})
