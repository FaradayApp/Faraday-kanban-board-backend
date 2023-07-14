from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from di import get_di_container
        container = get_di_container()
        container.wire(modules=[
            ".views"
        ])
