from django.http.response import HttpResponseForbidden
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import edit, DetailView, View

from users import forms
from users import models as users_models


class LoginView(edit.FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = '/users/home'

    def form_valid(self, form):
        login_status = form.login_user(request=self.request)
        if login_status:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RegisterView(edit.CreateView):
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('login')


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        user = request.user
        plans = users_models.Plans.objects.filter(user=user)

        return render(template_name='users/profile.html', request=request, context={'user': user, 'plans': plans})


class PlanView(edit.FormView):
    template_name = 'users/plan.html'
    form_class = forms.SelectProductForm
    success_url = 'plan-view'


# Get plan
# display details
# display form with product selection
# accept post request
