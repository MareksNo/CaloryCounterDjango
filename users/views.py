from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from django.views.generic import edit, DetailView, View, UpdateView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from users import forms
from users import models as users_models


class LoginView(edit.FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('profile-view')

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


class ProfileView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):

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


class CreatePlanView(LoginRequiredMixin, edit.CreateView):
    login_url = reverse_lazy('login')

    model = users_models.Plans
    fields = ['name', 'c_goal']
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(CreatePlanView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile')


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        messages.success(request=request, message='You have been logged out')
        logout(request=request)
        return HttpResponseRedirect(reverse('login'))


class AutoPlanView(LoginRequiredMixin, edit.FormView):
    login_url = reverse_lazy('login')

    template_name = 'users/plan_create_auto.html'
    form_class = forms.AutoPlanForm
    success_url = reverse_lazy('profile-view')

    def form_valid(self, form):
        gender_multipliers = {'f': {'age': 4.7, 'height': 4.7, 'weight': 4.35, 'bonus': 665},
                              'm': {'age': 6.8, 'height': 12.7, 'weight': 6.23, 'bonus': 66}}
        activity_multipliers = {'BMR': 1, 'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55, 'Very Active': 1.725}

        profile = users_models.Profile.objects.filter(user=self.request.user).first()

        gender = profile.gender
        weight = float(profile.weight)
        age = profile.age
        height = float(profile.height)
        activity = profile.activity

        bmr = weight * gender_multipliers[gender]['weight'] + height * gender_multipliers[gender]['height'] - age * gender_multipliers[gender]['age'] + gender_multipliers[gender]['bonus']
        if activity == 'BMR':
            plan = users_models.Plans.create_plan(name=form.cleaned_data['name'], c_goal=bmr, user=self.request.user)
            return HttpResponseRedirect(reverse('plan-view', kwargs={'pk': plan.id}))

        else:
            plan = users_models.Plans.create_plan(name=form.cleaned_data['name'], c_goal=bmr * activity_multipliers[activity], user=self.request.user)
            return HttpResponseRedirect(reverse('plan-view', kwargs={'pk': plan.id}))


class EditProfileView(LoginRequiredMixin, edit.UpdateView):
    pass


