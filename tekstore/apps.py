from django.apps import AppConfig

class TekstoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # اگر از Django 3.2+ استفاده می‌کنی
    name = 'tekstore'

    def ready(self):
        import tekstore.signals  # لود سیگنال‌ها هنگام اجرای اپ
