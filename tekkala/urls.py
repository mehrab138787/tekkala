from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # مسیرهای اپلیکیشن tekstore
    path('', include('tekstore.urls')),
]

# مسیر فایل‌های رسانه‌ای
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# مسیر فایل‌های استاتیک (در حالت توسعه)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
