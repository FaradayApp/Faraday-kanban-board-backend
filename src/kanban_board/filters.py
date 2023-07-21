import django_filters

from kanban_board import models


class TasksFilter(django_filters.FilterSet):
    class Meta:
        model = models.Task
        fields = ['status']
