from django.urls import path

from . import views

urlpatterns = [
    path('<str:user_name>/start', views.start, name='start'),
    path('<str:user_name>/ingame', views.ingame, name='ingame'),
    path('<str:user_name>/maps', views.maps, name='maps'),
    path('<str:user_name>/opbans', views.opbans, name='opbans'),
]
