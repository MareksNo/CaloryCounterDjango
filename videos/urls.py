from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from videos import views

urlpatterns = [
    path('video/<int:pk>/', views.VideoView.as_view(), name='display-video'),
    path('add_video', views.AddVideoView.as_view(), name='add-video')
]
