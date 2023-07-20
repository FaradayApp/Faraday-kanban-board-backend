from django.db import models

from utils.models import TimestampModel
from users.models import User


class TaskStatusTypes(models.IntegerChoices):
    BACKLOG = 1, ('backlog')
    TO_DO = 2, ('to_do')
    IN_PROGRESS = 3, ('in_progress')
    DONE = 4, ('done')
    ARCHIVE = 5, ('archive')


class TaskPriorityTypes(models.IntegerChoices):
    HIGH = 1, ('high')
    MEDIUM = 2, ('medium')
    LOW = 3, ('low')


class KanbanBoard(TimestampModel):
    group_id = models.CharField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='kanban_boards')


class Task(models.Model):
    board = models.ForeignKey(KanbanBoard, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    staging_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produced_tasks')
    performer = models.ManyToManyField(User, related_name='tasks')
    status = models.IntegerField(
        choices=TaskStatusTypes.choices,
        default=TaskStatusTypes.TO_DO
    )
    priority = models.IntegerField(
        choices=TaskPriorityTypes.choices,
        default=TaskPriorityTypes.MEDIUM
    )


class Comment(TimestampModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=600)
