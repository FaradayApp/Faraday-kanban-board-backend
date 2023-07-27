from django.urls import path, include
from rest_framework import routers

from kanban_board.views.board.board import KanbanBoardViewSet
from kanban_board.views.tasks.tasks import TasksViewSet


board_router = routers.SimpleRouter()
board_router.register(r'', KanbanBoardViewSet, basename='board')


tasks_router = routers.SimpleRouter()
tasks_router.register(r'(?P<board_uuid>[\w\-]+)/tasks', TasksViewSet, basename='tasks')


urlpatterns = [
    path('', include(board_router.urls)),
    path('', include(tasks_router.urls)),
]
