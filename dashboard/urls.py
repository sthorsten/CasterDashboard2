from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login', views.login, name='login'),

    path('home', views.home, name='home'),

    path('overlays/control-center', views.overlay_control_center, name='control-center')
]
