from django.urls import path

from . import views

urlpatterns = [
    path('<str:user_name>/ingame', views.ingame, name='ingame'),
]
