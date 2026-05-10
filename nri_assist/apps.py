from django.apps import AppConfig


class NriAssistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nri_assist'
    verbose_name = 'NRI Assist'

    def ready(self):
        import nri_assist.signals  # noqa: F401
