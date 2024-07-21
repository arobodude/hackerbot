from django.urls import path
from . import views

urlpatterns = [
        path("", views.home, name="home"),
        path('send_command/', views.send_command, name='send_command'),
        path('send_move_command/', views.send_move_command, name='send_move_command'),
        ]
