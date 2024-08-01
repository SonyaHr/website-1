from django.contrib import admin
from .models import Category, Tag, Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Реєстрація моделей з додатковими налаштуваннями

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('category', 'user', 'published_date')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    filter_horizontal = ('tags',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'published_date')
    search_fields = ('text', 'author__username')
    list_filter = ('post', 'author', 'published_date')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone')
    search_fields = ('user__username', 'telephone')

# Реєстрація моделей в адміністративній панелі
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)

# Реєстрація користувачів
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
