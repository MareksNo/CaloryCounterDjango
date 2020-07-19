from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def login_user(self, request):
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is not None:
            login(request=request, user=user)
            return True
        else:
            return False


class SelectProductForm(forms.Form):
    pass
