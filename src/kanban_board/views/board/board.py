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
        responses={status.HTTP_201_CREATED: KanbanBoardPreviewSerializer},
        description="""
            Метод для создания доски.
            Только для администратора.
            Создает новую канбан доску. Для создания необходимо передать title доски. 
            Возвращает информацию о доске, в том числе uuid доски, который нужен для работы с ней.
        """
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
        responses={status.HTTP_200_OK: KanbanBoardPreviewSerializer},
        description="""
            Метод для обновления информации о доске.
            Только для администратора.
            Обновляет информацию о доске.
            Возвращает объект доски с информацией о ней.
        """
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
    
    @extend_schema(
        request=CreateKanbanBoardSerializer,
        responses={status.HTTP_200_OK: KanbanBoardPreviewSerializer},
        description="""
            Метод для получения списка досок.
            Только для администратора.
            Возвращает список всех досок.
            В методе реализована пагинация, управлять которой можно с помощью параметров page и page_size
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        request=CreateKanbanBoardSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
        description="""
            Метод для удаления доски.
            Только для администратора.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
