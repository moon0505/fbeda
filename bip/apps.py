from django.apps import AppConfig


class BipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bip'


    def ready(self):
        # Make sure to replace 'bip.signals' with the correct path to your signals module.
        # This import statement ensures your signals are connected at startup.
        import bip.signals