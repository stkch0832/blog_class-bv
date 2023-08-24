from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=30)
    content = models.TextField('本文', max_length=500)
    image = models.ImageField('画像', upload_to='blog/images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
