from django.urls import path
from . import views

urlpatterns = [
        path("", views.home, name="home"),
        path('send_command/', views.send_command, name='send_command'),
        ]
