from pathlib import Path

from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
    path = str(Path(__file__).resolve().parent)
