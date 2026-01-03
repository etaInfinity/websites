from django.apps import AppConfig

class NpcgenConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "npcgen"

    def ready(self):
        from . import services  # noqa