from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=30,
        label='タイトル',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
        })
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
