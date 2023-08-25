from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='カテゴリ',  on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=30)
    content = models.TextField('本文', max_length=500)
    image = models.ImageField('画像', upload_to='blog/images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
