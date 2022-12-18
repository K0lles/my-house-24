from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from my_house_24 import settings
from .views import PageNotFoundView, InternalServerError

handler404 = PageNotFoundView.as_view()
handler505 = InternalServerError.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrator-panel/', include('administrator_panel.urls')),
    path('configuration/', include('configuration.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
