from django.urls import path

from products import views

urlpatterns = [
    path('add_food/', views.CreateFoodView.as_view(template_name='products/food_form.html'), name='add-food'),
]