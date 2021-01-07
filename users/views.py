from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from django.views.generic import edit, View
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.cache import cache

from users import forms
from users import models as users_models
from videos import models as video_models

User = get_user_model()


class LoginView(edit.FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('profile-view')

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return self.success_url  # return some other url if next parameter not present

    def form_valid(self, form):
        login_status = form.login_user(request=self.request)
        if login_status:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile-view')
        user_form = forms.UserForm
        profile_form = forms.ProfileForm

        return render(request=request, template_name='users/register.html', context={
            'form_user': user_form,
            'form_profile': profile_form,
            'action': 'Create User'
        })

    def post(self, request):
        form_user = forms.UserForm(request.POST)
        form_profile = forms.ProfileForm(request.POST)

        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()

            login(request=request, user=user)
            messages.success(request, message='Account created successfully')
            return HttpResponseRedirect(redirect_to=reverse('profile-view'))

        return render(request=request, template_name='users/user_form.html',
                      context={'form_user': form_user, 'form_profile': form_profile, 'action': 'Create Profile'})


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        user = request.user
        plans = cache.get(f'plans{user}')
        if not plans:
            plans = users_models.Plans.objects.filter(user=user)
            cache.set(f'plans{user}', plans, 600)
        videos = video_models.Video.objects.filter(user=user)
        return render(template_name='users/profile.html',
                      request=request,
                      context={'user': user,
                               'plans': plans,
                               'videos': videos
                               })


class PlanView(View):
    def get(self, request, pk):
        plan = get_object_or_404(users_models.Plans, pk=pk)
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
            amount = form.cleaned_data['amount']
            plan = get_object_or_404(users_models.Plans, pk=pk)

            statuses = {0: 'Reached', 1: 'Exceeded', -1: 'Not reached'}

            calories_status = plan.calories_status(calories_ct=food.calories, amount=amount)

            messages.success(request=request, message=f'You have added {amount} x {food.name} to your today\'s plan.')
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
        cache.delete(f'plans{self.request.user}')
        user = self.request.user
        form.instance.user = user
        return super(CreatePlanView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile-view')


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
        cache.delete(f'plans{self.request.user}')

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


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_instance = get_object_or_404(klass=User, pk=request.user.id)
        profile_instance = get_object_or_404(klass=users_models.Profile, user=request.user)

        form_user = forms.UserForm(instance=user_instance)
        form_profile = forms.ProfileForm(instance=profile_instance)

        return render(request=request, template_name='users/user_form.html', context={
            'form_user': form_user,
            'form_profile': form_profile,
            'action': 'Edit Profile'
        })

    def post(self, request):
        user_instance = get_object_or_404(klass=User, pk=request.user.id)
        profile_instance = get_object_or_404(klass=users_models.Profile, user=request.user)

        form_user = forms.UserForm(request.POST, instance=user_instance)
        form_profile = forms.ProfileForm(request.POST, instance=profile_instance)

        if form_user.is_valid() and form_profile.is_valid():
            form_profile.save()
            form_user.save()
            messages.success(request, message=f'Updated data for {user_instance.username} successfully')

        return render(request=request, template_name='users/user_form.html',
                      context={'form_user': form_user, 'form_profile': form_profile, 'action': 'Edit Profile'})
