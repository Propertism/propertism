from pathlib import Path

from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"
    path = str(Path(__file__).resolve().parent)
