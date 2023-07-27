from rest_framework import serializers

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry


class CreateKanbanBoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)

    def to_entry(self) -> CreateKanbanBoardEntry:
        return CreateKanbanBoardEntry(
            **self.validated_data
        )


class KanbanBoardPreviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = KanbanBoard
        fields = (
            'uuid',
            'title',
            'created_at'
        )
