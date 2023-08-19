from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class SignupUserForm(SignupForm):

    def save(self, request):
        user = super(SignupForm, self).save(request)

        # Profile インスタンス生成
        Profile.objects.create(user=user)

        return user


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user', 'created_at', 'updated_at')
        required = {
            'username': True,
        }
        labels = {
            'username': 'ユーザー名',
            'introduction': '自己紹介',
            'birth': '生年月日',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control my-3'
                    }
                ),
            'introduction': forms.Textarea(
                attrs={
                    'class': 'form-control my-3',
                    'rows': 6,
                    'cols': 50
                    }
                ),
            'birth': forms.NumberInput(
                attrs={
                    'class': 'form-control my-3',
                    'type': 'date',
                    }
                ),
        }
