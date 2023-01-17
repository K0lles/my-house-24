from django.contrib import messages
from django.shortcuts import render

from administrator_panel.mixins import *
from .forms import *


class MainPageUpdateView(PermissionUpdateView):
    model = MainPage
    template_name = 'site_management/main-page-update.html'
    form_class = MainPageForm
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        obj = MainPage.objects.select_related('seo').first()
        if not obj:
            obj = MainPage.objects.create()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_form'] = SeoForm(prefix='seo', instance=self.object.seo)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, request.FILES, instance=self.object)
        seo_form = SeoForm(request.POST, prefix='seo', instance=self.object.seo)
        if form.is_valid() and seo_form.is_valid():
            return self.form_valid(form, seo_form)
        return self.form_invalid(form, seo_form)

    def form_valid(self, form, seo_form):
        main_page = form.save(commit=False)
        seo = seo_form.save()
        main_page.seo = seo
        main_page.save()
        messages.success(self.request, 'Зміни успішно збережено.')
        return redirect('main-page-update')

    def form_invalid(self, form, seo_form):
        messages.error(self.request, 'Виникли помилки. Перевірте правильність вхідних даних.')
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        context['seo_form'] = seo_form
        return self.render_to_response(context)
