from pathlib import Path

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    path = str(Path(__file__).resolve().parent)
