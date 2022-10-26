from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView

from .models import *
from .forms import *


class MeasurementUnitListView(CreateView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'configuration/measurement_unit-list.html'

    def get_context_data(self, **kwargs):
        measurement_unit_queryset = MeasurementUnit.objects.all().order_by('id')
        context = super(MeasurementUnitListView, self).get_context_data(**kwargs)
        context['formset'] = measurement_unit_formset(measurement_unit_queryset.exists())(queryset=measurement_unit_queryset)
        return context

    def post(self, request, *args, **kwargs):
        measurement_unit_queryset = MeasurementUnit.objects.all().order_by('id')
        unit_formset = measurement_unit_formset(measurement_unit_queryset.exists())
        formset = unit_formset(request.POST, queryset=measurement_unit_queryset)

        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data.get('name'):
                    form.save()
            return redirect('measurement-units')

        self.object = None
        context = self.get_context_data(**kwargs)
        context['formset'] = formset
        return self.render_to_response(context)


class MeasurementUnitDeleteView(DeleteView):
    model = MeasurementUnit
    template_name = 'configuration/measurement_unit-list.html'
    pk_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        try:
            unit_to_delete = MeasurementUnit.objects.get(pk=kwargs['pk'])
            if not unit_to_delete.is_used:
                unit_to_delete.delete()
            else:
                raise MeasurementUnit.DoesNotExist
        except MeasurementUnit.DoesNotExist:
            return JsonResponse({'answer': 'failed'})
        return JsonResponse({'answer': 'success'})


class ServiceCreateListView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'configuration/service-list.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceCreateListView, self).get_context_data(**kwargs)
        service_list = Service.objects.select_related('measurement_unit').all().order_by('id')
        context['service_list'] = service_list
        context['measurement_units'] = MeasurementUnit.objects.all().order_by('id')
        context['formset'] = service_formset(service_list.exists())(queryset=service_list)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        formset = service_formset(context['service_list'].exists())(request.POST, queryset=context['service_list'])
        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data.get('name') and form.cleaned_data.get('measurement_unit'):
                    form_saved = form.save()
                    unit = MeasurementUnit.objects.get(pk=form_saved.measurement_unit.id)
                    unit.is_used = True
                    unit.save()
            return redirect('services')
        context['formset'] = formset
        return self.render_to_response(context)


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'configuration/service-list.html'
    pk_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        try:
            service_to_delete = Service.objects.select_related('measurement_unit').get(pk=kwargs['pk'])
            if service_to_delete.is_used:
                raise Service.DoesNotExist()
            service_to_delete.delete()
            related_measurement_unit = MeasurementUnit.objects.prefetch_related('service_set').get(pk=service_to_delete.measurement_unit.pk)
            if not related_measurement_unit.service_set.all().exists():
                related_measurement_unit.is_used = False
                related_measurement_unit.save()
        except Service.DoesNotExist:
            return JsonResponse({'answer': 'failed'})
        return JsonResponse({'answer': 'success'})


class TariffCreateView(CreateView):
    model = Tariff
    template_name = 'configuration/tariff-create-update.html'
    form_class = TariffForm

    def get_object(self, queryset=None):
        try:
            return Tariff.objects.prefetch_related('tariffservice_set').get(pk=self.kwargs.get('pk'))
        except Tariff.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super(TariffCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('tariff_id'):
            tariff = Tariff.objects.prefetch_related('tariffservice_set',
                                                     'tariffservice_set__service')\
                .get(pk=self.request.GET.get('tariff_id'))
            context['tariff_to_copy'] = tariff
        context['services'] = Service.objects.select_related('measurement_unit').all()
        context['formset'] = tariff_service_formset(queryset=TariffService.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = tariff_service_formset(request.POST, queryset=TariffService.objects.none())
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset=formset)
        context = self.get_context_data()
        context['form'] = form
        context['formset'] = formset
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        tariff_saved = None
        if form.cleaned_data.get('name') and form.cleaned_data.get('description'):
            tariff_saved = form.save()

        for form in kwargs['formset']:
            if form.cleaned_data.get('service') and form.cleaned_data.get('price') and tariff_saved:
                saved_service_tariff = form.save(commit=False)
                saved_service_tariff.tariff = tariff_saved
                saved_service_tariff.service.is_used = True
                saved_service_tariff.service.save()
                saved_service_tariff.save()

        return redirect('tariffs')


class TariffListView(ListView):
    queryset = Tariff.objects.all().order_by('updated_at')
    template_name = 'configuration/tariff-list.html'


class TariffDetailView(DetailView):
    model = Tariff
    template_name = 'configuration/tariff-detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        return Tariff.objects.prefetch_related('tariffservice_set',
                                               'tariffservice_set__service',
                                               'tariffservice_set__service__measurement_unit').get(pk=self.kwargs.get('pk'))


class TariffUpdateView(UpdateView):
    model = Tariff
    template_name = 'configuration/tariff-create-update.html'
    pk_url_kwarg = 'pk'
    form_class = TariffForm

    def get_object(self, queryset=None):
        try:
            return Tariff.objects.prefetch_related('tariffservice_set',
                                                   'tariffservice_set__service',
                                                   'tariffservice_set__service__measurement_unit').get(pk=self.kwargs.get(self.pk_url_kwarg))
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': self.model._meta.verbose_name})

    def get_context_data(self, **kwargs):
        context = super(TariffUpdateView, self).get_context_data(**kwargs)
        context['services'] = Service.objects.select_related('measurement_unit').all()
        tariff_services = context['object'].tariffservice_set.all()
        # if self.object:
        #     tariff_services = context['object'].tariffservice_set.all()
        # else:
        #     tariff_services = self.get_object().tariffservice_set.all()
        context['tariff_services'] = tariff_services
        context['formset'] = tariff_service_formset(queryset=tariff_services)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        form = self.form_class(request.POST, instance=self.get_object())
        formset = tariff_service_formset(request.POST, queryset=self.get_object().tariffservice_set.all())
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form=form, formset=formset)
        context['form'] = form
        context['formset'] = formset
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        tariff_saved = self.get_object()
        if form.cleaned_data.get('name') and form.cleaned_data.get('description'):
            tariff_saved = form.save()

        for form in kwargs['formset']:
            if form.cleaned_data.get('service') and form.cleaned_data.get('price') and tariff_saved:
                saved_service_tariff = form.save(commit=False)
                saved_service_tariff.tariff = tariff_saved
                saved_service_tariff.service.is_used = True
                saved_service_tariff.service.save()
                saved_service_tariff.save()

        return redirect('tariffs')


def tariff_delete(request, pk):
    try:
        tariff_to_delete = Tariff.objects.get(pk=pk)
        tariff_to_delete.delete()
    except TariffService.DoesNotExist:
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})


def tariff_service_delete(request, pk_tariff_service_to_delete):
    try:
        tariff_service_to_delete = TariffService.objects.get(pk=pk_tariff_service_to_delete)
        tariff_service_to_delete.delete()
    except TariffService.DoesNotExist:
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})


class RolesListUpdate(ListView):
    model = Role
    template_name = 'configuration/role-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RolesListUpdate, self).get_context_data()
        context['formset'] = role_formset(queryset=Role.objects.all().exclude(role__in=['user', 'owner']))
        return context

    def post(self, request, *args, **kwargs):
        formset = role_formset(request.POST, queryset=Role.objects.all().exclude(role__in=['user', 'owner']))
        if formset.is_valid():
            formset.save()
            return redirect('roles')
        self.object_list = None
        context = self.get_context_data()
        context['formset'] = formset
        return self.render_to_response(context)


class UserCreateView(CreateView):
    model = User
    template_name = 'configuration/user-create.html'
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            self.form_valid(form)
            return redirect('users')
        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        User.objects.create_user(email=form.cleaned_data.get('email'),
                                 password=form.cleaned_data.get('password'),
                                 name=form.cleaned_data.get('name'),
                                 surname=form.cleaned_data.get('surname'),
                                 phone=form.cleaned_data.get('phone'),
                                 status=form.cleaned_data.get('status'),
                                 role=form.cleaned_data.get('role'))


class UserUpdateView(UpdateView):
    model = User
    template_name = 'configuration/user-create.html'
    form_class = UserForm
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        try:
            user = User.objects.select_related('role').get(pk=self.kwargs['pk'])
            return user
        except User.DoesNotExist:
            raise Http404()

    def get_form(self, form_class=None):
        return UserForm(instance=self.get_object())

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance=self.get_object())
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data)
        return redirect('users')


class UserListView(ListView):
    model = User
    template_name = 'configuration/user-list.html'

    def get_queryset(self):
        return User.objects.select_related('role').all().order_by('pk')


class PaymentRequisitesCreateView(CreateView):
    model = PaymentRequisite
    template_name = 'configuration/payment-requisite.html'
    form_class = PaymentRequisitesForm

    def get_form(self, form_class=None):
        return PaymentRequisitesForm(instance=PaymentRequisite.objects.first())

    def post(self, request, *args, **kwargs):
        form = PaymentRequisitesForm(request.POST, instance=PaymentRequisite.objects.first())
        if form.is_valid():
            form.save()
            return redirect('requisites')
        self.object = None
        return self.render_to_response(self.get_context_data())


class ArticlePaymentCreateView(CreateView):
    model = ArticlePayment
    template_name = 'configuration/article-payment-create-update.html'
    form_class = ArticlePaymentForm

    def get_form(self, form_class=None):
        return ArticlePaymentForm()

    def post(self, request, *args, **kwargs):
        form = ArticlePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles-payment')
        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ArticlePaymentListView(ListView):
    model = ArticlePayment
    template_name = 'configuration/article-payment-list.html'
    queryset = ArticlePayment.objects.all().order_by('pk')


class ArticlePaymentUpdateView(UpdateView):
    model = ArticlePayment
    template_name = 'configuration/article-payment-create-update.html'
    form_class = ArticlePaymentForm
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        try:
            return ArticlePayment.objects.get(pk=self.kwargs['pk'])
        except (KeyError, ArticlePayment.DoesNotExist):
            raise Http404()

    def post(self, request, *args, **kwargs):
        form = ArticlePaymentForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect('articles-payment')
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


def delete_article(request, pk):
    try:
        article_to_delete = ArticlePayment.objects.get(pk=pk)
        article_to_delete.delete()
    except ArticlePayment.DoesNotExist:
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})
