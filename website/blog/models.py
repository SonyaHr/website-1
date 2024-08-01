from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="тег")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="заголовок")
    content = models.TextField(verbose_name="опис")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default='1')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name="Теги", blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "пости"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    telephone = models.CharField(max_length=10, default="+380-00-000-00-00", unique=True)
    reputation = models.IntegerField(default=0) 

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="Автор")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Photo(models.Model):
    image = models.ImageField(upload_to="photos")

    def __str__(self):
        return self.image.name
    
class PostImage (models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='пост')
    image = models.ImageField(upload_to='post.images/', blank=True, null=True, verbose_name='зображення')
    
    def _str_(self):
        return f"Image for {self.post.title}"
    
    class Meta:
        verbose_name = "зображення поста"
        verbose_name_plural = "зображення постів"