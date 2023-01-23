from django.contrib import messages
from django.http import Http404

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
        return self.form_invalid(form)

    def form_valid(self, form, seo_form, photo_form, additional_photo_form, document_formset):
        about_us = form.save(commit=False)
        seo = seo_form.save()
        about_us.seo = seo

        if not self.object.gallery:
            about_us.gallery = Gallery.objects.create(name='about-us-gallery')
        if not self.object.additional_gallery:
            about_us.additional_gallery = Gallery.objects.create(name='about-us-additional-gallery')
        about_us.save()

        if photo_form.cleaned_data.get('photo'):
            photo = photo_form.save(commit=False)
            photo.gallery = about_us.gallery
            photo.save()
        if additional_photo_form.cleaned_data.get('photo'):
            additional_photo = additional_photo_form.save(commit=False)
            additional_photo.gallery = about_us.additional_gallery
            additional_photo.save()

        for document in document_formset.forms:
            if document.cleaned_data.get('title') and document.cleaned_data.get('file'):
                document_saved = document.save(commit=False)
                document_saved.about_us = about_us
                document_saved.save()
        messages.success(self.request, 'Зміни успішно збережені.')
        return redirect('about-us-update')

    def form_invalid(self, form):
        messages.error(self.request, 'Щось пішло не так при. Перевірте правильність вводу.')
        return redirect('about-us-update')


class PhotoDeleteView(PermissionDeleteView):
    model = Photo
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        try:
            return Photo.objects.get(pk=self.kwargs.get('photo_pk'))
        except Photo.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Фото успішно видалено.')
        return redirect('about-us-update')


class DocumentDeleteView(PermissionDeleteView):
    model = Document
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        try:
            return Document.objects.get(pk=self.kwargs.get('document_pk'))
        except Document.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Документ успішно видалено.')
        return redirect('about-us-update')


class ServiceFrontUpdateView(PermissionUpdateView):
    model = ServiceFront
    template_name = 'site_management/service-front-update.html'
    form_class = ServiceFrontForm
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        obj = ServiceFront.objects.first()
        if not obj:
            obj = ServiceFront.objects.create()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_form'] = SeoForm(prefix='seo', instance=self.object.seo)
        context['service_front_object_formset'] = service_object_front_formset_factory(queryset=ServiceObjectFront.objects.filter(service_front=self.object), prefix='service-object')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, instance=self.object)
        seo_form = SeoForm(request.POST, instance=self.object.seo, prefix='seo')
        service_front_object_formset = service_object_front_formset_factory(
            request.POST,
            request.FILES,
            prefix='service-object',
            queryset=ServiceObjectFront.objects.filter(service_front=self.object)
        )
        if form.is_valid() and seo_form.is_valid() and service_front_object_formset.is_valid():
            return self.form_valid(form, seo_form, service_front_object_formset)
        return self.form_invalid(form)

    def form_valid(self, form, seo_form, service_front_object_formset):
        seo = seo_form.save()
        service = form.save(commit=False)
        if not self.object.seo:
            service.seo = seo
        service.save()

        for obj in service_front_object_formset.forms:
            if obj.cleaned_data.get('photo') and obj.cleaned_data.get('title') and obj.cleaned_data.get('description'):
                obj_saved = obj.save(commit=False)
                obj_saved.service_front = self.object
                obj_saved.save()

        messages.success(self.request, 'Зміни успішно збережені.')
        return redirect('service-front-update')

    def form_invalid(self, form):
        messages.error(self.request, 'Щось пішло не так. Перевірте правильність вводу.')
        return redirect('service-front-update')


class ServiceObjectFrontDeleteView(PermissionDeleteView):
    model = ServiceObjectFront
    string_permission = 'site_management_access'

    def get_object(self, queryset=None):
        try:
            return ServiceObjectFront.objects.get(pk=self.kwargs.get('service_object_pk'))
        except ServiceObjectFront.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Послугу успішно видалено.')
        return redirect('service-front-update')
