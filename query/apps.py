from django.apps import AppConfig


class QueryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "query"

    def ready(self):
        import query.signals
