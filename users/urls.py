from django.urls import path

from users import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(template_name='users/user_form.html'), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile-view'),
    path('plan/', views.PlanView.as_view(), name='plan-view'),
]
