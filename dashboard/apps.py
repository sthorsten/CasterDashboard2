from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        import dashboard.models.receivers
