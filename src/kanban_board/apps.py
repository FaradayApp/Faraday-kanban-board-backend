from django.apps import AppConfig


class KanbanBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kanban_board'

    def ready(self):
        from di import get_di_container
        container = get_di_container()
        # container.wire(modules=[  # TODO ADD VIEWS
        # ])
