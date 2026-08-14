from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .handlers import handle_post_migrate


class BirthdayConfig(AppConfig):
    name = "birthday"
    verbose_name = "Birthday"

    def ready(self):
        post_migrate.connect(
            handle_post_migrate,
            dispatch_uid="birthday.handlers.handle_post_migrate",
        )
