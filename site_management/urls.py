from django.urls import path

from .views import *


urlpatterns = [
    path('main-page/', MainPageUpdateView.as_view(), name='main-page-update'),
    path('about-us/', AboutUsUpdateView.as_view(), name='about-us-update'),
]
