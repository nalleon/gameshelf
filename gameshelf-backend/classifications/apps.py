from django.apps import AppConfig


class ClassificationsConfig(AppConfig):
    name = 'classifications'

    def ready(self):
        from . import signals
