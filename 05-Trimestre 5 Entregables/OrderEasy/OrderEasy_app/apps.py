from django.apps import AppConfig


class OrdereasyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OrderEasy_app'


class OrdereasyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OrderEasy_app'

    def ready(self):
        import OrderEasy_app.signals