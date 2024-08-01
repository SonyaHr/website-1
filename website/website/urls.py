from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('shop.urls', namespace='shop')),  # Домашня сторінка магазину
    path('orders/', include('orders.urls', namespace='orders')),
    path('blog/', include('blog.urls', namespace='blog')),  # Додаємо URL для блогу
    path('gallery/', include('gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
