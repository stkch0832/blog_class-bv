from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from . models import User
from . forms import SignupUserForm
from allauth.account import views

class IndexView(TemplateView):
    template_name = "accounts/index.html"


# Account
class SignupView(views.SignupView):
    template_name = "account/signup.html"
    from_class = SignupUserForm

class LoginView(views.LoginView):
    template_name = 'account/login.html'


class LogoutView(views.LogoutView):
    template_name = 'account/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('accounts:index')
