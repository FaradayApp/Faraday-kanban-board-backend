from rest_framework import serializers

from kanban_board.services.comments.entries import CommentEntry
from users.serializers import UserSerializer



class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=600)
    user =  UserSerializer(many=False, read_only=True)

    def to_entry(self) -> CommentEntry:
        return CommentEntry(
            **self.validated_data
        )
