from django.apps import AppConfig

class SearchingPartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'searchingPart'

    def ready(self):
        import searchingPart.signals  # Import signals when app is ready