from django.urls import path, include

from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control

from users import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile-view', ),
    path('plan/<int:pk>/', views.PlanView.as_view(), name='plan-view'),
    path('create-plan/', views.CreatePlanView.as_view(), name='create-plan-view'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('auto_setup/', views.AutoPlanView.as_view(), name='auto-plan'),
    path('edit_user/', views.EditProfileView.as_view(), name='edit-user'),
    path('register/', views.RegisterView.as_view(), name='register'),


    # REST Framework URLS
    path('api/plan/', include('users.api.urls', 'plans_api'))
]
