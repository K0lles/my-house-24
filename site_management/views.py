from django.shortcuts import render

from administrator_panel.mixins import *
from .forms import *


class MainPageUpdateView(PermissionUpdateView):
    model = MainPage
    template_name = 'site_management/main-page-update.html'
    form_class = MainPageForm
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        obj = MainPage.objects.first()
        if not obj:
            obj = MainPage.objects.create()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_form'] = SeoForm(prefix='seo')
        return context
