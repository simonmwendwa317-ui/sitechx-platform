from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authx.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/geo/', include('apps.geo.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('health/', include('apps.authx.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
