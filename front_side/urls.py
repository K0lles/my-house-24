from django.urls import path

from .views import *


urlpatterns = [
    path('', MainPageDetailView.as_view(), name='main-page'),
    path('about-us/', AboutUsPageDetailView.as_view(), name='about-us-page'),
    path('service/', ServiceFrontPageDetailView.as_view(), name='service-page'),
    path('contact/', ContactPageDetailView.as_view(), name='contact-page')
]
