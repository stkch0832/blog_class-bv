from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from . models import Profile
from . forms import SignupUserForm, ProfileForm
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin

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


# Profile
class ProfileDetailView(View):
    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.get(user_id=request.user.id)
        return render(request, 'accounts/profile_detail.html', context={
            'user_id': request.user.id,
            'profile_data': profile_data,
            })


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.get(user_id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'username': profile_data.username,
                'introduction': profile_data.introduction,
                'birth': profile_data.birth,
            }
        )

        return render(request, 'accounts/profile_form.html', context={
            'user_id': request.user.id,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)

        if form.is_valid():
            profile_data = Profile.objects.get(user_id=request.user.id)
            profile_data.username = form.cleaned_data['username']
            profile_data.introduction = form.cleaned_data['introduction']
            profile_data.birth = form.cleaned_data['birth']
            profile_data.save()
            return redirect('accounts:profile_detail', request.user.id)

        return render(request, 'accounts/profile_form.html', context={
            'form': form,
        })
