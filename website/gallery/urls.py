from django.urls import path
from .views import gallery, media

urlpatterns = [
    path('', gallery, name='gallery'),
    path('media/', media, name='media'),
]
