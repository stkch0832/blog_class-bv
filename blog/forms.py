from django import forms
from django.contrib.auth import get_user_model
from .models import Category

User = get_user_model()

class ArticleForm(forms.Form):
    category_data = Category.objects.all()
    category_choice = {}
    for category in category_data:
        category_choice[category] = category

    title = forms.CharField(
        max_length=30,
        label='タイトル',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
        })
        )
    category = forms.ChoiceField(
        label='カテゴリ',
        widget=forms.Select,
        choices=list(category_choice.items())
    )
    content = forms.CharField(
        max_length=500,
        label='内容',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-3',
            'rows': 10,
            'cols': 50,
        })
    )
    image = forms.ImageField(
        label='画像',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control mb-3',
        })
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='',
        max_length=255,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-3',
            'rows': 6,
            'cols': 50,
        })
    )
