from django import forms
from django.contrib.auth import authenticate, login
from products import models as product_models
from users import models as user_models
from django.contrib.auth.models import User


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
    product = forms.ModelChoiceField(queryset=product_models.Food.objects.all(), empty_label='Choose')
    amount = forms.IntegerField(min_value=1, label='Amount')


class AutoPlanForm(forms.Form):
    name = forms.CharField(label='Plan Name')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = user_models.Profile
        fields = ['weight', 'height', 'age', 'gender', 'activity']


# https://docs.djangoproject.com/en/3.0/ref/models/fields/#choices
