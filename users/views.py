from django.http.response import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from django.views.generic import edit, DetailView, View, UpdateView

from users import forms
from users import models as users_models


class LoginView(edit.FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = '/users/profile'

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


class PlanView(View):
    def get(self, request, pk):
        plan = get_object_or_404(users_models.Plans, pk=pk)
        print(request.user)
        print(plan.user)
        if not request.user == plan.user:
            messages.error(message='Please login to access this plan!', request=request)
            return redirect('login')

        form = forms.SelectProductForm
        context = {
            'plan': plan,
            'form': form,
        }
        return render(request=request, template_name='users/plans_detail.html', context=context)

    def post(self, request, pk):
        form = forms.SelectProductForm(request.POST)
        if form.is_valid():
            food = form.cleaned_data['product']
            plan = get_object_or_404(users_models.Plans, pk=pk)

            statuses = {0: 'Reached', 1: 'Exceeded', -1: 'Not reached'}

            calories_status = plan.calories_status(calories_ct=food.calories)

            messages.success(request=request, message=f'You have added {food.name} to your today\'s plan.')
            messages.info(request=request, message=f'Status of your plan: {statuses[calories_status]}')

            context = {
                'plan': plan,
                'form': form,
            }

            return render(request=request, template_name='users/plans_detail.html', context=context)


class AddPlanView(edit.CreateView):
    model = users_models.Plans
    fields = ['name', 'c_goal']

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddPlanView, self).get(request=request)
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(AddPlanView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile')


