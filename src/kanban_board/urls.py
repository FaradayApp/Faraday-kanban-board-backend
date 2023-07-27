from django.urls import path, include
from rest_framework import routers

from kanban_board.views.board.board import CreateKanbanBoardAPI
from kanban_board.views.tasks.tasks import TasksViewSet


albums_router = routers.SimpleRouter()
albums_router.register(r'(?P<board_uuid>[\w\-]+)/tasks', TasksViewSet, basename='tasks')


board_urls = [
    path('', CreateKanbanBoardAPI.as_view(), name='create-board'),
]


urlpatterns = [
    path('', include(board_urls)),
    path('', include(albums_router.urls)),
]
