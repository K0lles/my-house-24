from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('administrator-panel/', include('administrator_panel.urls')),
    path('configuration/', include('configuration.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]
