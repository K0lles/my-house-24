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


class AboutUsUpdateView(PermissionUpdateView):
    model = AboutUs
    template_name = 'site_management/about-us-update.html'
    form_class = AboutUsForm
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        obj = AboutUs.objects.select_related('seo', 'gallery').first()
        if not obj:
            obj = AboutUs.objects.create()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_form'] = SeoForm(prefix='seo', instance=self.object.seo)
        context['document_formset'] = document_formset_factory(prefix='document', queryset=Document.objects.filter(about_us=self.object))
        context['photo_form'] = PhotoForm(prefix='photo')
        context['photos'] = Photo.objects.filter(gallery=self.object.gallery)
        context['additional_photo_form'] = PhotoForm(prefix='additional-photo')
        context['additional_photos'] = Photo.objects.filter(gallery=self.object.additional_gallery)
        # photo_formset_factory = modelformset_factory(Photo, PhotoForm, extra=1 if not Photo.objects.filter(gallery=self.object.gallery).exists() else 0)
        # context['photo_formset'] = photo_formset_factory(prefix='photo', queryset=Photo.objects.filter(gallery=self.object.gallery))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, request.FILES, instance=self.object)
        seo_form = SeoForm(request.POST, prefix='seo', instance=self.object.seo)
        photo_form = PhotoForm(request.POST, request.FILES, prefix='photo')
        additional_photo_form = PhotoForm(request.POST, request.FILES, prefix='additional-photo')
        document_formset = document_formset_factory(request.POST, request.FILES, prefix='document', queryset=Document.objects.filter(about_us=self.object))
        if form.is_valid() and seo_form.is_valid() and photo_form.is_valid() and additional_photo_form.is_valid() and document_formset.is_valid():
            return self.form_valid(form, seo_form, photo_form, additional_photo_form, document_formset)
        print(f'form: {form.errors}')
        print(f'seo-form: {seo_form.errors}')
        print(f'photo_form: {photo_form.errors}')
        print(f'additional_photo_form: {additional_photo_form.errors}')
        print(f'document_formset: {document_formset.errors}')
        return redirect('about-us-update')

    def form_valid(self, form, seo_form, photo_form, additional_photo_form, document_formset):
        about_us = form.save(commit=False)
        seo = seo_form.save()
        about_us.seo = seo

