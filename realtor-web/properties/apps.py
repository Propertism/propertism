from pathlib import Path

from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "properties"
    path = str(Path(__file__).resolve().parent)
