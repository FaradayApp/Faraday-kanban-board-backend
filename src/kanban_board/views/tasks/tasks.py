from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from dependency_injector.wiring import Provide, inject
from drf_spectacular.utils import extend_schema

from di import Container
from kanban_board.serializers.tasks import CreateTaskSerializer, TaskSerializer
from kanban_board.services.tasks.create_task import CreateTaskCommand
from kanban_board.services.tasks.repo import TaskRepo

from utils.mixins import CustomCreateModelMixin, CustomUpdateModelMixin
from utils import pagination


class TasksViewSet(
    CustomCreateModelMixin,
    # CustomUpdateModelMixin,
    # mixins.ListModelMixin,
    # mixins.RetrieveModelMixin,
    GenericViewSet
):
    pagination_class = pagination.DefaultPagination

    def get_queryset(self, repo: TaskRepo = Provide[Container.task_repo]):
        return repo.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        # elif self.action in ('update', 'partial_update'):
        #     return EditTaskSerializer
        # elif self.action == 'list':
        #     return PreviewTaskSerializer
        # return TaskSerializer

    @extend_schema(
        request=CreateTaskSerializer,
        responses={status.HTTP_201_CREATED: TaskSerializer}
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
            board_id=self.kwargs.get('board_id'),
            task_data=serializer.to_entry()
        )
        return TaskSerializer(task, many=False, context={'request': self.request})

    # @extend_schema(
    #     request=EditTaskSerializer,
    #     responses={status.HTTP_200_OK: TaskSerializer}
    # )
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @inject
    # def perform_update(
    #     self,
    #     serializer: EditTaskSerializer,
    #     service: EditTaskCommand = Provide[Container.edit_task]
    # ):
    #     task = service(
        #     user=self.request.user,
        #     board_id=self.kwargs.get('board_id'),
        #     task_data=serializer.to_entry()
        # )
        
    #     return serializers.TaskSerializer(post, many=False, context={'request': self.request})
