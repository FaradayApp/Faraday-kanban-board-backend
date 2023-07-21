from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from rest_framework.response import Response
from dependency_injector.wiring import Provide, inject
from drf_spectacular.utils import extend_schema

from di import Container
from kanban_board.serializers.board import CreateKanbanBoardSerializer, KanbanBoardPreviewSerializer
from kanban_board.services.board.create_board import CreateKanbanBoardCommand


class CreateKanbanBoardAPI(APIView):
    @extend_schema(
        request=CreateKanbanBoardSerializer,
        responses={status.HTTP_201_CREATED: KanbanBoardPreviewSerializer}
    )
    def post(
            self,
            request, 
            service: CreateKanbanBoardCommand = Provide[Container.create_board],
            ):
        serializer = CreateKanbanBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        board = service(board_data=serializer.to_entry(), user=request.user)

        return Response(status=status.HTTP_201_CREATED, data=KanbanBoardPreviewSerializer(board).data)
