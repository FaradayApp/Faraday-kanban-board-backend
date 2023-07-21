from rest_framework import serializers

from kanban_board.models import Task
from kanban_board.services.tasks.entries import CreateTaskEntry


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


class TaskSerializer(serializers.ModelSerializer):  # TODO comments and users

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
        )
