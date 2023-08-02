import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from kanban_board import models


User = get_user_model()


class TasksFilter(django_filters.FilterSet):
    class Meta:
        model = models.Task
        fields = ['status']

    order_by = django_filters.OrderingFilter(
        fields=(
            ('expiration_date', 'expiration_date'),
            ('priority', 'priority'),
        )
    )


class UsersInBoardFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_user')

    def search_user(self, queryset, _, value):
        return queryset.filter(
            Q(username__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value)
        )
    
    class Meta:
        model = User
        fields = ['search']
