from django import forms
from allauth.account.forms import SignupForm


class SignupUserForm(SignupForm):

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.save()
        return user
