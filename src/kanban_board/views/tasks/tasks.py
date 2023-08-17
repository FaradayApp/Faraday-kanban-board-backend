from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from dependency_injector.wiring import Provide, inject
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from di import Container
from kanban_board.filters import TasksFilter
from kanban_board.serializers.tasks import CreateTaskSerializer, EditTaskSerializer, TaskSerializer, PreviewTaskSerializer
from kanban_board.services.board.repo import KanbanBoardRepo
from kanban_board.services.tasks.create_task import CreateTaskCommand
from kanban_board.services.tasks.edit_task import EditTaskCommand
from kanban_board.services.tasks.repo import TaskRepo

from utils.mixins import CustomCreateModelMixin, CustomUpdateModelMixin
from utils import pagination


class TasksViewSet(
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    pagination_class = pagination.DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TasksFilter

    @inject
    def get_queryset(
            self,
            repo: TaskRepo = Provide[Container.task_repo],
            board_repo: KanbanBoardRepo = Provide[Container.board_repo],
            ):
        board = board_repo.get_board_by_uuid(uuid=self.kwargs.get('board_uuid'))
        board_repo.check_user_in_board(board=board, user=self.request.user)
        if self.action == 'list':
            return repo.add_comments_count(repo.all(board=board))
        return repo.all(board=board)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        elif self.action in ('update', 'partial_update'):
            return EditTaskSerializer
        elif self.action == 'list':
            return PreviewTaskSerializer
        return TaskSerializer

    @extend_schema(
        request=CreateTaskSerializer,
        responses={status.HTTP_201_CREATED: TaskSerializer},
        description="""
            Метод для создания задачи.
            Метод принимает информацию о задаче и создает ее в базе данных, прикрепляя к ней необходимых пользователей, как исполнителей. 
            Создателя задачи прикрепляет, как ее постановщика.
            Возвращает информацию о задаче.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @inject
    def perform_create(
        self,
        serializer: CreateTaskSerializer,
        service: CreateTaskCommand = Provide[Container.create_task]
    ):
        task = service(
            user=self.request.user,
            board_uuid=self.kwargs.get('board_uuid'),
            task_data=serializer.to_entry()
        )
        return TaskSerializer(task, many=False, context={'request': self.request})

    @extend_schema(
        request=EditTaskSerializer,
        responses={status.HTTP_200_OK: TaskSerializer},
        description="""
            Метод для обновления задачи.
            Логика работы метода отличается от пользователя вызывающего его.
            Для создателя задачи, принимает обновленную информацию о задаче и меняет ее в базе данных.
            Остальные пользователи могут только изменить статус задачи.
            Возвращает информацию о задаче.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @inject
    def perform_update(
        self,
        serializer: EditTaskSerializer,
        service: EditTaskCommand = Provide[Container.edit_task]
    ):

        task = service(
            user=self.request.user,
            task=serializer.instance,
            board_uuid=self.kwargs.get('board_uuid'),
            task_data=serializer.to_entry()
        )
        
        return TaskSerializer(task, many=False, context={'request': self.request})
    
    @extend_schema(
        responses={status.HTTP_200_OK: TaskSerializer},
        description="""
            Метод для получения списка задач в доске.
            Возвращает список всех задач доски.
            В методе реализована пагинация, управлять которой можно с помощью параметров page и page_size
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: TaskSerializer},
        description="""
            Метод для получения задачи.
            Возвращает подробную информацию о задаче.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
