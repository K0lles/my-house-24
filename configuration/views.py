from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.db.models import ProtectedError
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import random

from administrator_panel.mixins import *
from .forms import *
from .tokens import *


class MeasurementUnitListView(PermissionCreateView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'configuration/measurement_unit-list.html'
    string_permission = 'service_access'

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


class MeasurementUnitDeleteView(PermissionDeleteView):
    model = MeasurementUnit
    template_name = 'configuration/measurement_unit-list.html'
    pk_url_kwarg = 'pk'
    string_permission = 'service_access'

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


class ServiceCreateListView(PermissionCreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'configuration/service-list.html'
    string_permission = 'service_access'

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


class ServiceDeleteView(PermissionDeleteView):
    model = Service
    template_name = 'configuration/service-list.html'
    pk_url_kwarg = 'pk'
    string_permission = 'service_access'

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
        except (Service.DoesNotExist, ProtectedError):
            return JsonResponse({'answer': 'failed'})
        return JsonResponse({'answer': 'success'})


class TariffCreateView(PermissionCreateView):
    model = Tariff
    template_name = 'configuration/tariff-create-update.html'
    form_class = TariffForm
    string_permission = 'tariff_access'

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


class TariffListView(PermissionListView):
    queryset = Tariff.objects.all().order_by('updated_at')
    template_name = 'configuration/tariff-list.html'
    string_permission = 'tariff_access'


class TariffDetailView(PermissionDetailView):
    model = Tariff
    template_name = 'configuration/tariff-detail.html'
    pk_url_kwarg = 'pk'
    string_permission = 'tariff_access'

    def get_object(self, queryset=None):
        return Tariff.objects.prefetch_related('tariffservice_set',
                                               'tariffservice_set__service',
                                               'tariffservice_set__service__measurement_unit').get(pk=self.kwargs.get('pk'))


class TariffUpdateView(PermissionUpdateView):
    model = Tariff
    template_name = 'configuration/tariff-create-update.html'
    pk_url_kwarg = 'pk'
    form_class = TariffForm
    string_permission = 'tariff_access'

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
    if request.user.is_anonymous or not request.user.role.tariff_access:
        return JsonResponse({'answer': 'Ви не маєте доступу до тарифів'})
    try:
        tariff_to_delete = Tariff.objects.get(pk=pk)
        tariff_to_delete.delete()
    except TariffService.DoesNotExist:
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})


def tariff_service_delete(request, pk_tariff_service_to_delete):
    if request.user.is_anonymous or not request.user.role.tariff_access:
        return JsonResponse({'answer': 'Ви не маєте доступу до тарифів'})
    try:
        tariff_service_to_delete = TariffService.objects.get(pk=pk_tariff_service_to_delete)
        tariff_service_to_delete.delete()
    except TariffService.DoesNotExist:
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})


class RolesListUpdate(PermissionListView):
    model = Role
    template_name = 'configuration/role-list.html'
    string_permission = 'role_access'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RolesListUpdate, self).get_context_data()
        context['formset'] = role_formset(queryset=Role.objects.all().exclude(role__in=['user', 'owner']))
        return context

    def post(self, request, *args, **kwargs):
        formset = role_formset(request.POST, queryset=Role.objects.all().exclude(role__in=['user', 'owner']))
        if formset.is_valid():
            for form in formset.forms:
                form_saved = form.save(commit=False)
                if form_saved.role != 'director':
                    form_saved.save()
            return redirect('roles')
        self.object_list = None
        context = self.get_context_data()
        context['formset'] = formset
        return self.render_to_response(context)


class UserCreateView(PermissionCreateView):
    model = User
    template_name = 'configuration/user-create-update.html'
    form_class = UserForm
    string_permission = 'user_access'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
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


class UserDetailView(PermissionDetailView):
    model = User
    template_name = 'configuration/user-detail.html'
    pk_url_kwarg = 'pk'
    string_permission = 'user_access'

    def get_object(self, queryset=None):
        try:
            return User.objects.select_related('role').get(pk=self.kwargs['pk'])
        except (User.DoesNotExist, ValueError):
            raise Http404()


class UserUpdateView(PermissionUpdateView):
    model = User
    template_name = 'configuration/user-create-update.html'
    form_class = UserForm
    pk_url_kwarg = 'pk'
    string_permission = 'user_access'

    def get_object(self, queryset=None):
        try:
            return User.objects.select_related('role').get(pk=self.kwargs['pk'])
        except User.DoesNotExist:
            raise Http404()

    def get_form(self, form_class=None):
        return UserForm(instance=self.get_object())

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            return self.form_valid(form, user)
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, user):
        old_password = user.password
        user_saved = form.save()
        if form.cleaned_data.get('password'):
            user_saved.set_password(form.cleaned_data.get('password'))
            user_saved.save()
        else:
            user_saved.password = old_password
            user_saved.save()
        return redirect('users')


class UserListView(PermissionListView):
    model = User
    template_name = 'configuration/user-list.html'
    string_permission = 'user_access'

    def get_queryset(self):
        return User.objects.select_related('role').all().order_by('pk')


def delete_user(request, pk):
    if request.user.is_anonymous or not request.user.role.user_access:
        return JsonResponse({'answer': 'Ви не маєте доступу до користувачів'})
    try:
        user = User.objects.get(pk=pk)
        user.delete()
    except (User.DoesNotExist, ValueError):
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})


class PaymentRequisitesCreateView(PermissionCreateView):
    model = PaymentRequisite
    template_name = 'configuration/payment-requisite.html'
    form_class = PaymentRequisitesForm
    string_permission = 'payment_requisite_access'

    def get_form(self, form_class=None):
        return PaymentRequisitesForm(instance=PaymentRequisite.objects.first())

    def post(self, request, *args, **kwargs):
        form = PaymentRequisitesForm(request.POST, instance=PaymentRequisite.objects.first())
        if form.is_valid():
            form.save()
            return redirect('requisites')
        self.object = None
        return self.render_to_response(self.get_context_data())


class ArticlePaymentCreateView(PermissionCreateView):
    model = ArticlePayment
    template_name = 'configuration/article-payment-create-update.html'
    form_class = ArticlePaymentForm
    string_permission = 'payment_requisite_access'

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


class ArticlePaymentListView(PermissionListView):
    model = ArticlePayment
    template_name = 'configuration/article-payment-list.html'
    queryset = ArticlePayment.objects.all().order_by('pk')
    string_permission = 'payment_requisite_access'


class ArticlePaymentUpdateView(PermissionUpdateView):
    model = ArticlePayment
    template_name = 'configuration/article-payment-create-update.html'
    form_class = ArticlePaymentForm
    pk_url_kwarg = 'pk'
    string_permission = 'payment_requisite_access'

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
    if request.user.is_anonymous or not request.user.role.payment_requisite_access:
        return JsonResponse({'answer': 'Ви не маєте доступу до користувачів'})
    try:
        article_to_delete = ArticlePayment.objects.get(pk=pk)
        article_to_delete.delete()
    except (ArticlePayment.DoesNotExist, ProtectedError):
        return JsonResponse({'answer': 'failed'})
    return JsonResponse({'answer': 'success'})


class UserLoginView(CreateView):
    model = User
    template_name = 'configuration/user-login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role.role == 'owner':
                return redirect('owner-receipts')
            return redirect('statistics')
        self.object = None
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return self.errors_occurred()

            if not user.check_password(password):
                user = None

            if user and user.role.role == 'owner' and user.status != 'disconnected':
                if not user.is_active:
                    messages.error(request, 'Ваш обліковий запис не підтверджений! Перегляньте ваші листи на пошті та підтвердіть його.')
                    return redirect('user-login')
                login(request, user)
                if not request.POST.get('remember_me'):
                    self.request.session.set_expiry(0)
                return redirect('owner-receipts')
        self.object = None
        context = self.get_context_data()
        context['error'] = 'Неправильно введені дані'
        return self.render_to_response(context=context)

    def errors_occurred(self):
        self.object = None
        context = self.get_context_data()
        context['error'] = 'Неправильно введені дані'
        return self.render_to_response(context=context)


class ManagementLoginView(CreateView):
    model = User
    template_name = 'configuration/user-staff-login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if request.user.role.role == 'owner':
                return redirect('owner-receipts')
            return redirect('statistics')
        self.object = None
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(username=email,
                                password=password)
            if user and user.role.role != 'owner' and user.status != 'disconnected':
                login(request, user)
                if not request.POST.get('remember_me'):
                    self.request.session.set_expiry(0)
                return redirect('statistics')
        self.object = None
        context = self.get_context_data()
        context['error'] = 'Неправильно введені дані'
        return self.render_to_response(context=context)


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('user-login')


def send_activation_mail(request, user, to_mail):
    message_subject = 'Підтвердіть ваш обліковий запис.'
    message_with_template = render_to_string("email-activation-template.html", {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(message_subject, message_with_template, to=[to_mail])
    email.content_subtype = 'html'
    if email.send(fail_silently=True):
        messages.success(request, 'Користувач зареєстрований. Підтвердіть із вказаної пошти ваш обліковий запис для закінчення реєстрації')
    else:
        messages.error(request, 'Не вдалося відправити підтвердження на пошту. Перевірте правильність введення email')


class UserActivation(View):

    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs.get('uidb64')))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and account_activation_token.check_token(user, self.kwargs.get('token')):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Ваш облікований запис підтверджено. Ввійдіть у свій обліковий запис знову.')
            return redirect('user-login')
        else:
            messages.error(self.request, 'Підтвердження облікового запису не відбулося.')
        return redirect('user-login')


class UserRegistrationView(CreateView):
    model = User
    template_name = 'configuration/user-registration.html'
    form_class = UserSelfRegistrationForm

    @staticmethod
    def rand_x_digit_num(x: int, leading_zeroes=True):
        """Return an X digit number, leading_zeroes returns a string, otherwise int"""
        if not leading_zeroes:
            return str(random.randint(10 ** (x - 1), 10 ** x - 1))
        else:
            if x > 6000:
                return ''.join([str(random.randint(0, 9)) for i in range(x)])
            else:
                return '{0:0{x}d}'.format(random.randint(0, 10 ** x - 1), x=x)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.role.role == 'owner':
                return redirect('owner-receipts')
            return redirect('statistics')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        user = User.objects.create_user(owner_id=UserRegistrationView.rand_x_digit_num(8),
                                        email=form.cleaned_data.get('email'),
                                        name=form.cleaned_data.get('name'),
                                        surname=form.cleaned_data.get('surname'),
                                        password=form.cleaned_data.get('password'),
                                        is_active=False,
                                        role=Role.objects.get(role='owner'),)
        send_activation_mail(self.request, user, user.email)
        return redirect('user-registration')

    def form_invalid(self, form):
        messages.error(self.request, 'Щось пішло не так. Перевірте правильність вводу даних')
        self.object = None
        context = self.get_context_data()
        return self.render_to_response(context)
