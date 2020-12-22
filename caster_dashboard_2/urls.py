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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from caster_dashboard_2.settings.base import *
from dashboard.views import sites, forms

urlpatterns = [
    path('', sites.index),
    path('login/', sites.login_view),
    path('login/form', forms.login_form),
    path('register/', sites.register),
    path('register/form', forms.register_form),
    path('register/success', sites.register_success),
    path('logout/', sites.logout_view),

    # Errors
    path('500', sites.error_500, name='500'),
    path('404', sites.error_404, name='404'),

    path('dashboard/', include('dashboard.urls')),
    path('overlays/', include('overlays.urls')),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

handler404 = sites.error_404
handler500 = sites.error_500
