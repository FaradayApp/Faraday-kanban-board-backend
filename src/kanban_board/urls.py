from django.urls import path, include

from kanban_board.views.board.board import CreateKanbanBoardAPI


board_urls = [
    path('', CreateKanbanBoardAPI.as_view(), name='create-board'),
]


urlpatterns = [
    path('', include(board_urls)),
]
