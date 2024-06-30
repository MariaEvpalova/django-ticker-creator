from django.urls import path
from .views import create_video

urlpatterns = [
    path('create_video/', create_video, name='create_video'),
]
