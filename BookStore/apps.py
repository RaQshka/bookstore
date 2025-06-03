from django.apps import AppConfig

class BookStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BookStore'

    def ready(self):
        import BookStore.signals