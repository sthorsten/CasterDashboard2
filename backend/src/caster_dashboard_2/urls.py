from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    # Backend urls
    path('admin/', admin.site.urls),
    path('api/v2/', include('api.urls')),

    # Admin Home (default route)
    path('', RedirectView.as_view(url='/admin/', permanent=True), name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
