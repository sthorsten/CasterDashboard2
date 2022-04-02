from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

from core.channels import CoreConsumer
from main.channels import MainConsumer
from match.channels import MatchConsumer
from overlays.channels import OverlaysConsumer

from dashboard import views

urlpatterns = [
    # Errors
    path('500', views.error_500, name='500'),
    path('404', views.error_404, name='404'),

    # Backend urls
    path('admin/', admin.site.urls),
    path('api/v2/', include('api.urls')),

    # Admin Home (default route)
    path('', RedirectView.as_view(url='/admin/', permanent=True), name='index'),
]

websocket_urlpatterns = [
    re_path(r'ws/core/$', CoreConsumer.as_asgi()),
    re_path(r'ws/main/$', MainConsumer.as_asgi()),
    re_path(r'ws/match/$', MatchConsumer.as_asgi()),
    re_path(r'ws/overlays/$', OverlaysConsumer.as_asgi())
]

handler404 = views.error_404
handler500 = views.error_500
