from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from dependency_injector.wiring import Provide, inject
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from di import Container
from kanban_board.serializers.comments import CommentSerializer
from kanban_board.services.board.repo import KanbanBoardRepo
from kanban_board.services.comments.create_comment import CreateCommentCommand
from kanban_board.services.comments.edit_comment import EditCommentCommand
from kanban_board.services.comments.repo import CommentsRepo
from kanban_board.services.tasks.repo import TaskRepo

from utils.mixins import CustomCreateModelMixin, CustomUpdateModelMixin
from utils import exceptions, pagination


class CommentsViewSet(
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pagination_class = pagination.DefaultPagination

    @inject
    def get_queryset(
            self,
            repo: CommentsRepo = Provide[Container.comments_repo],
            board_repo: KanbanBoardRepo = Provide[Container.board_repo],
            task_repo: TaskRepo = Provide[Container.task_repo],
            ):
        board = board_repo.get_board_by_uuid(uuid=self.kwargs.get('board_uuid'))
        board_repo.check_user_in_board(board=board, user=self.request.user)
        task = task_repo.get_task_by_id(id=self.kwargs.get('task_id'))
        return repo.all(task=task)
    
    def get_object(self):
        obj = super().get_object()
        if self.action in ('update', 'partial_update', 'destroy') and obj.user != self.request.user:
            raise exceptions.CustomException('Permission denied')
        return obj

    def get_serializer_class(self):
        return CommentSerializer

    @extend_schema(
        request=CommentSerializer,
        responses={status.HTTP_201_CREATED: CommentSerializer},
        description="""
            Метод для создания комментария.
            Принимает текст комментария, создает его в базе данных подставляя отправителя запроса, как его создателя.
            Возвращает комментарий.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @inject
    def perform_create(
        self,
        serializer: CommentSerializer,
        service: CreateCommentCommand = Provide[Container.create_comment]
    ):
        comment = service(
            user=self.request.user,
            task_id=self.kwargs.get('task_id'),
            comment_data=serializer.to_entry()
        )
        return CommentSerializer(comment, many=False, context={'request': self.request})

    @extend_schema(
        request=CommentSerializer,
        responses={status.HTTP_200_OK: CommentSerializer},
        description="""
            Метод для обновления комментария.
            Только для создателя комментария.
            Принимает новый текст комментария и меняет его в базе данных.
            Возвращает комментарий.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @inject
    def perform_update(
        self,
        serializer: CommentSerializer,
        service: EditCommentCommand = Provide[Container.edit_comment]
    ):
        comment = service(
            user=self.request.user,
            comment=serializer.instance,
            comment_data=serializer.to_entry()
        )
        
        return CommentSerializer(comment, many=False, context={'request': self.request})
    
    @extend_schema(
        responses={status.HTTP_200_OK: CommentSerializer},
        description="""
            Метод для получения списка комментариев к задаче.
            Возвращает список комментариев, оставленных в определенной задаче.
            В методе реализована пагинация, управлять которой можно с помощью параметров page и page_size
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None},
        description="""
            Метод для удаления комментария.
            Только для создателя комментария.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
