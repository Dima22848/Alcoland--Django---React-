from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'Аккаунт'
    verbose_name_plural = 'Аккаунты'

    def ready(self):
        import account.signals  # Импортируем сигналы