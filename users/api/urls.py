from django.urls import path

from users.api.views import api_detail_plan_view

app_name = 'users'

urlpatterns = [
    path('<pk>', api_detail_plan_view, name='detail')
]
