from django.shortcuts import render
from django.views.generic import DetailView

from site_management.models import *


class MainPageDetailView(DetailView):
    model = MainPage
    template_name = 'front_side/base_page_front.html'

    def get_object(self, queryset=None):
        return MainPage.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        return context


class AboutUsPageDetailView(DetailView):
    model = AboutUs
    template_name = 'front_side/about-us.html'

    def get_object(self, queryset=None):
        return AboutUs.objects.prefetch_related('gallery__photo_set', 'additional_gallery__photo_set').first()


class ServiceFrontPageDetailView(DetailView):
    model = ServiceFront
    template_name = 'front_side/service.html'

    def get_object(self, queryset=None):
        return ServiceFront.objects.prefetch_related('serviceobjectfront_set').first()


class ContactPageDetailView(DetailView):
    model = Contact
    template_name = 'front_side/contact.html'

    def get_object(self, queryset=None):
        return Contact.objects.first()
