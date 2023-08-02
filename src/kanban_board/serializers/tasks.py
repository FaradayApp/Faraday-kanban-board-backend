from rest_framework import serializers

from kanban_board.models import Task
from kanban_board.serializers.comments import CommentSerializer
from kanban_board.services.tasks.entries import CreateTaskEntry, EditTaskEntry
from users.serializers import UserSerializer


class CreateTaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60)
    description = serializers.CharField(max_length=1000, required=False)
    expiration_date = serializers.DateField()
    performers = serializers.ListField(child=serializers.IntegerField())
    status = serializers.IntegerField(min_value=1, max_value=5)
    priority = serializers.IntegerField(min_value=1, max_value=3)

    def to_entry(self) -> CreateTaskEntry:
        return CreateTaskEntry(
            **self.validated_data
        )


class EditTaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    expiration_date = serializers.DateField(required=False)
    performers = serializers.ListField(child=serializers.IntegerField(), required=False)
    status = serializers.IntegerField(min_value=1, max_value=5, required=False)
    priority = serializers.IntegerField(min_value=1, max_value=3, required=False)

    def to_entry(self) -> EditTaskEntry:
        return EditTaskEntry(
            **self.validated_data
        )


class TaskSerializer(serializers.ModelSerializer):
    producer = UserSerializer(many=False, read_only=True)
    performers = UserSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'staging_date',
            'expiration_date',
            'status',
            'priority',
            'producer',
            'performers',
            'description',
            'comments',
        )


class PreviewTaskSerializer(serializers.ModelSerializer):
    performers = UserSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'expiration_date',
            'status',
            'priority',
            'performers',
            'comments_count'
        )
