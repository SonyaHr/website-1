from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .views import MyLogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    # Головна сторінка
    path('', views.index, name='index'),
    
    # Перегляд окремого посту
    path('post/<str:name>/', views.post, name='post'),
    
    # Контактна сторінка
    path('contacts/', views.contact, name='contacts'),

    # Перегляд постів за категорією
    path("category/<str:c>", views.category, name="category"),
    
    # Пошук постів
    path("search", views.search, name="search"),
    
    # Створення нового посту
    path("create", views.create, name="create"),
    
    # Авторизація користувача
    path("login", LoginView.as_view(template_name='blog/login.html'), name="blog_login"),
    
    # Вихід з аккаунту
    path("logout", MyLogoutView.as_view(), name="blog_logout"),
    
    # Профіль користувача
    path("profile", views.profile, name="profile"),
    
    # Оновлення профілю користувача
    path("update-profile", views.edit_profile, name="edit_profile"),
    
    # Реєстрація нового користувача
    path("registration", views.registration, name="registration"),
    
    # Галерея
    path("gallery", views.gallery, name="gallery"),
    
    # Профіль едіт
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    path('comment/upvote/<int:id>/', views.comment_upvote, name='comment_upvote'),
    
    path('comment/downvote/<int:id>/', views.comment_downvote, name='comment_downvote'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
