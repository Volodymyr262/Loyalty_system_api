from django.apps import AppConfig

class LoyaltyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "loyalty"  #  Ensure this matches your actual app name

    def ready(self):
        from . import signals