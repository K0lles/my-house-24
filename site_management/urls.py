from django.urls import path

from .views import *


urlpatterns = [
    path('main-page/', MainPageUpdateView.as_view(), name='main-page-update'),
    path('about-us/', AboutUsUpdateView.as_view(), name='about-us-update'),
    path('photo/delete/<int:photo_pk>/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('document/delete/<int:document_pk>/', DocumentDeleteView.as_view(), name='document-delete'),
    path('service/', ServiceFrontUpdateView.as_view(), name='service-front-update'),
    path('service-object/delete/<int:service_object_pk>/', ServiceObjectFrontDeleteView.as_view(), name='service-object-front-delete'),
]
