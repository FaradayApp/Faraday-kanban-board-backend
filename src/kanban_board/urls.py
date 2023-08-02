from django.urls import path, include
from rest_framework import routers

from kanban_board.views.board.board import KanbanBoardViewSet
from kanban_board.views.tasks.tasks import TasksViewSet
from kanban_board.views.users.users import UsersInBoardViewSet


board_router = routers.SimpleRouter()
board_router.register(r'', KanbanBoardViewSet, basename='board')


tasks_router = routers.SimpleRouter()
tasks_router.register(r'(?P<board_uuid>[\w\-]+)/tasks', TasksViewSet, basename='tasks')


users_board_router = routers.SimpleRouter()
users_board_router.register(r'(?P<board_uuid>[\w\-]+)/users', UsersInBoardViewSet, basename='users-in-board')


urlpatterns = [
    path('', include(board_router.urls)),
    path('', include(tasks_router.urls)),
    path('', include(users_board_router.urls)),
]
