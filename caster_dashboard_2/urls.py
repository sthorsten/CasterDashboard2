"""caster_dashboard_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('login/form', views.login_form),
    path('register/', views.register),
    path('register/form', views.register_form),
    path('register/success', views.register_success),
    path('logout/', views.logout_view),

    path('dashboard/', include('dashboard.urls')),
    path('overlays/', include('overlays.urls')),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
