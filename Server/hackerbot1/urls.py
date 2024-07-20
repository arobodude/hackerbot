from django.urls import path
from . import views

urlpatterns = [
        path("", views.home, name="home"),
        path('print_command/', views.print_command, name='print_command'),
        ]
