from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    user = models.ManyToManyField(User, blank=True)
    resource = models.TextField(max_length=50)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def __str__(self) -> str:
        return self.resource

class Post(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    published = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    viewed = models.ManyToManyField(User, blank=True)
    
    class Meta:
        ordering = ['rating']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self) -> str:
        return self.text

class Digest(models.Model):
    posts = models.ManyToManyField(Post)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated']
        verbose_name = 'Дайджест'
        verbose_name_plural = 'Дайджесты'