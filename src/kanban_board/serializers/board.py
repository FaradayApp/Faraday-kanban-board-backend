from rest_framework import serializers

from kanban_board.models import KanbanBoard
from kanban_board.services.board.entries import CreateKanbanBoardEntry


class CreateKanbanBoardSerializer(serializers.Serializer):
    group_id = serializers.CharField(max_length=256)

    def to_entry(self) -> CreateKanbanBoardEntry:
        return CreateKanbanBoardEntry(
            **self.validated_data
        )


class KanbanBoardPreviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = KanbanBoard
        fields = (
            'id',
            'created_at'
        )
