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
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

from caster_dashboard_2.settings import MEDIA_URL, MEDIA_ROOT
from dashboard import views

urlpatterns = [
    # Errors
    path('500', views.error_500, name='500'),
    path('404', views.error_404, name='404'),

    # Backend urls
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    url(r'^jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # API Home (default route)
    url(r'^.$', RedirectView.as_view(url='/api/', permanent=True), name='index'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

handler404 = views.error_404
handler500 = views.error_500
