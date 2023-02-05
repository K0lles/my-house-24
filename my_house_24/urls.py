from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from my_house_24 import settings
from .views import PageNotFoundView, InternalServerError

from site_management.sitemaps import *


sitemaps = {
    'main_page': MainPageSitemap,
    'about_us': AboutUpsSitemap,
    'service': ServiceSitemap,
    'contact': ContactSitemap,
}

handler404 = PageNotFoundView.as_view()
handler505 = InternalServerError.as_view()

urlpatterns = [
    path('', include('front_side.urls')),
    path('administrator-panel/', include('administrator_panel.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('configuration/', include('configuration.urls')),
    path('site-management/', include('site_management.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
