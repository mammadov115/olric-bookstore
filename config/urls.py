from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),  # TODO: Change this in production
    
    # API
    # path('api/v1/', include('apps.api.urls')),
    
    # Apps
    # path('', include('apps.pages.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('books/', include('apps.books.urls')),
    # path('cart/', include('apps.cart.urls')),
    # path('orders/', include('apps.orders.urls')),
]

# Serve media files in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
