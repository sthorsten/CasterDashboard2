from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.urls import path
from rest_framework import routers, serializers, viewsets
from api.serializers import *

from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Overlays
    path('overlay/overlay_state/<int:user_id>/', views.overlay_state),
    path('overlay/timer_overlay_data/<int:user_id>/', views.timer_overlay_data),
    path('overlay/current_match/<int:user_id>/', views.set_current_match),
    path('overlay/next_match/<int:user_id>/', views.set_next_match),
]
