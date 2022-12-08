import openpyxl

from django.db.models import Q, Count, Sum, Func, F, Value, Case, When, FloatField, Subquery, OuterRef, QuerySet
from django.db.models.functions import Concat
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models.deletion import ProtectedError
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from configuration.models import Role, Tariff, Service, MeasurementUnit
from .forms import *
from my_house_24 import settings


class HouseCreateView(CreateView):
    model = House
    template_name = 'administrator_panel/house-create-update.html'
    form_class = HouseForm

    def get_context_data(self, **kwargs):
        context = super(HouseCreateView, self).get_context_data(**kwargs)
        context['user_formset'] = house_user_formset(queryset=HouseUser.objects.none(), prefix='users')
        context['section_formset'] = section_formset(queryset=Section.objects.none(), prefix='sections')
        context['floor_formset'] = floor_formset(queryset=Floor.objects.none(), prefix='floors')
        context['users'] = User.objects.select_related('role').all()

        # dictionary for parsing js dictionary on frontend for changeUser function
        context['user_role_dict'] = {'none': ''}  # starter value
        for user in context['users']:
            context['user_role_dict'][user.pk] = user.role.get_role_display()
        context['roles'] = Role.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = HouseForm(request.POST, request.FILES or None)
        user_formset_post = house_user_formset(request.POST, queryset=HouseUser.objects.none(), prefix='users')
        section_formset_post = section_formset(request.POST, queryset=Section.objects.none(), prefix='sections')
        floor_formset_post = floor_formset(request.POST, queryset=Floor.objects.none(), prefix='floors')

        if form.is_valid() and user_formset_post.is_valid() and section_formset_post.is_valid() \
                and floor_formset_post.is_valid():
            house = self.form_valid(form=form,
                                    user_formset_post=user_formset_post,
                                    section_formset_post=section_formset_post,
                                    floor_formset_post=floor_formset_post)
            return redirect('house-detail', house_pk=house.pk)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        context['user_formset'] = user_formset_post
        context['floor_formset'] = floor_formset_post
        context['section_formset'] = section_formset_post
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        house = form.save()  # is used for selecting foreign key of new form in formsets

        for form in kwargs['user_formset_post']:
            if form.cleaned_data.get('user'):
                user_house_saved = form.save(commit=False)
                user_house_saved.house = house
                user_house_saved.save()

        for form in kwargs['section_formset_post']:
            if form.cleaned_data.get('name'):
                section_saved = form.save(commit=False)
                section_saved.house = house
                section_saved.save()

        for form in kwargs['floor_formset_post']:
            if form.cleaned_data.get('name'):
                floor_saved = form.save(commit=False)
                floor_saved.house = house
                floor_saved.save()

        return house


class HouseUpdateView(UpdateView):
    model = House
    template_name = 'administrator_panel/house-create-update.html'
    pk_url_kwarg = 'house_pk'
    form_class = HouseForm

    def get_object(self, queryset=None):
        try:
            return House.objects.prefetch_related('houseuser_set', 'houseuser_set__user', 'houseuser_set__user__role',
                                                  'floor_set', 'section_set').get(pk=self.kwargs['house_pk'])
        except (House.DoesNotExist, ValueError, AttributeError):
            raise Http404()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(HouseUpdateView, self).get_context_data(**kwargs)
        context['user_formset'] = house_user_formset(queryset=self.object.houseuser_set.all(), prefix='users')
        context['section_formset'] = section_formset(queryset=self.object.section_set.all(), prefix='sections')
        context['floor_formset'] = floor_formset(queryset=self.object.floor_set.all(), prefix='floors')
        context['users'] = User.objects.select_related('role').all()

        # dictionary for parsing js dictionary on frontend for changeUser function
        context['user_role_dict'] = {'none': ''}  # starter value
        for user in context['users']:
            context['user_role_dict'][user.pk] = user.role.get_role_display()
        context['roles'] = Role.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = HouseForm(request.POST, request.FILES or None, instance=self.object)
        user_formset_post = house_user_formset(request.POST, queryset=self.object.houseuser_set.all(), prefix='users')
        section_formset_post = section_formset(request.POST, queryset=self.object.section_set.all(), prefix='sections')
        floor_formset_post = floor_formset(request.POST, queryset=self.object.floor_set.all(), prefix='floors')

        if form.is_valid() and user_formset_post.is_valid() and section_formset_post.is_valid() \
                and floor_formset_post.is_valid():
            self.form_valid(form=form,
                            user_formset_post=user_formset_post,
                            section_formset_post=section_formset_post,
                            floor_formset_post=floor_formset_post)
            return redirect('house-detail', house_pk=self.kwargs['house_pk'])

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        context['user_formset'] = user_formset_post
        context['floor_formset'] = floor_formset_post
        context['section_formset'] = section_formset_post
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        house = form.save()  # is used for selecting foreign key of new form in formsets

        for form in kwargs['user_formset_post']:
            if form.cleaned_data.get('user'):
                user_house_saved = form.save(commit=False)
                user_house_saved.house = house
                user_house_saved.save()

        for form in kwargs['section_formset_post']:
            if form.cleaned_data.get('name'):
                section_saved = form.save(commit=False)
                section_saved.house = house
                section_saved.save()

        for form in kwargs['floor_formset_post']:
            if form.cleaned_data.get('name'):
                floor_saved = form.save(commit=False)
                floor_saved.house = house
                floor_saved.save()


class HouseDetailView(DetailView):
    model = House
    template_name = 'administrator_panel/house-detail.html'
    pk_url_kwarg = 'house_pk'

    def get_object(self, queryset=None):
        try:
            return House.objects.prefetch_related('houseuser_set', 'houseuser_set__user', 'houseuser_set__user__role',
                                                  'floor_set', 'section_set').get(pk=self.kwargs['house_pk'])
        except (House.DoesNotExist, ValueError, AttributeError):
            raise Http404()


class HouseListView(ListView):
    model = House
    queryset = House.objects.all()
    template_name = 'administrator_panel/house-list.html'


def delete_house(request, house_pk):
    try:
        house = House.objects.get(pk=house_pk)
        house.delete()
        return JsonResponse({'answer': 'success'})
    except (ValueError, AttributeError, House.DoesNotExist, ProtectedError):
        return JsonResponse({'answer': 'failed'})


def delete_section(request, section_pk):
    try:
        section_to_delete = Section.objects.get(pk=section_pk)
        section_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except (ValueError, AttributeError, Section.DoesNotExist):
        return JsonResponse({'answer': 'failed'})


def delete_floor(request, floor_pk):
    try:
        floor_to_delete = Floor.objects.get(pk=floor_pk)
        floor_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except (ValueError, AttributeError, Floor.DoesNotExist):
        return JsonResponse({'answer': 'failed'})


def delete_house_user(request, house_user_pk):
    try:
        house_user_to_delete = HouseUser.objects.get(pk=house_user_pk)
        house_user_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except (ValueError, AttributeError, HouseUser.DoesNotExist):
        return JsonResponse({'answer': 'failed'})


class FlatCreateView(CreateView):
    model = Flat
    template_name = 'administrator_panel/flat-create-update.html'
    form_class = FlatForm

    def get_context_data(self, **kwargs):
        context = super(FlatCreateView, self).get_context_data(**kwargs)
        houses = House.objects.prefetch_related('floor_set', 'section_set', 'flat_set').all()
        house_section = {}
        house_floor = {}
        for house in houses:
            house_section[house.pk] = []
            for section in house.section_set.all():
                house_section[house.pk].append([section.pk, section.name])
        for house in houses:
            house_floor[house.pk] = []
            for floor in house.floor_set.all():
                house_floor[house.pk].append([floor.pk, floor.name])
        context['owners'] = User.objects.filter(role__role='owner')
        context['tariffs'] = Tariff.objects.all()
        context['houses'] = houses
        context['house_section'] = house_section
        context['house_floor'] = house_floor
        context['personal_accounts'] = PersonalAccount.objects.filter(flat__isnull=True)
        if self.request.GET.get('prev_flat'):
            context['base_flat'] = Flat.objects.select_related('section',
                                                               'floor',
                                                               'house',
                                                               'owner').prefetch_related('house__floor_set',
                                                                                         'house__section_set').get(
                pk=self.request.GET.get('prev_flat'))
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = FlatForm(request.POST)
        if form.is_valid():
            return self.form_valid(form, personal_account_number=request.POST.get('personal-account'))
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, personal_account_number):
        created_flat = form.save()
        if personal_account_number:
            try:
                account = PersonalAccount.objects.get(number=personal_account_number)
                if not account.flat:
                    account.flat = created_flat
                    account.status = 'active'
                    account.save()
            except PersonalAccount.DoesNotExist:
                PersonalAccount.objects.create(number=personal_account_number,
                                               flat=created_flat,
                                               status='active')
        if self.request.POST.get('create-again') == 'create-new':
            return redirect(f'{reverse("flat-create")}?prev_flat={created_flat.pk}')
        return redirect('flat-detail', flat_pk=created_flat.pk)


class FlatDetailView(DetailView):
    model = Flat
    template_name = 'administrator_panel/flat-detail.html'
    pk_url_kwarg = 'flat_pk'

    def get_object(self, queryset=None):
        try:
            return Flat.objects.select_related('house', 'section', 'floor', 'owner', 'personalaccount').get(
                pk=self.kwargs['flat_pk'])
        except Flat.DoesNotExist:
            raise Http404()


class FlatListView(ListView):
    model = Flat
    template_name = 'administrator_panel/flat-list.html'
    queryset = Flat.objects.select_related('house', 'section', 'floor', 'owner', 'personalaccount').all().order_by('-id')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FlatListView, self).get_context_data(object_list=object_list, **kwargs)
        personal_accounts = calculate_notoriety_and_receipt_sum(PersonalAccount.objects.select_related('flat').filter(flat__isnull=False, status='active')).get('personal_accounts')
        context['object_list'] = context['object_list']\
            .annotate(
            rest=Subquery(personal_accounts.filter(pk=OuterRef('personalaccount__id')).values('rest')[:1]),
            receipt_sum=Subquery(personal_accounts.filter(pk=OuterRef('personalaccount__id')).values('receipt_sum')[:1]),
            subtraction=Case(When(rest__isnull=True, then=Value(0.00)), default='rest', output_field=FloatField()) -
                    Case(When(receipt_sum__isnull=True, then=Value(0.00)), default='receipt_sum',
                         output_field=FloatField()))
        return context


class FlatUpdateView(UpdateView):
    model = Flat
    template_name = 'administrator_panel/flat-create-update.html'
    form_class = FlatForm
    pk_url_kwarg = 'flat_pk'

    def get_object(self, queryset=None):
        try:
            return Flat.objects.get(pk=self.kwargs['flat_pk'])
        except Flat.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        flat = self.get_object()
        context = super(FlatUpdateView, self).get_context_data(**kwargs)
        houses = House.objects.prefetch_related('floor_set', 'section_set', 'flat_set').all()
        house_section = {}
        house_floor = {}
        for house in houses:
            house_section[house.pk] = []
            for section in house.section_set.all():
                house_section[house.pk].append([section.pk, section.name])
        for house in houses:
            house_floor[house.pk] = []
            for floor in house.floor_set.all():
                house_floor[house.pk].append([floor.pk, floor.name])
        try:
            context['selected_account'] = PersonalAccount.objects.get(flat=flat)
        except PersonalAccount.DoesNotExist:
            context['selected_account'] = None
        context['owners'] = User.objects.filter(role__role='owner')
        context['tariffs'] = Tariff.objects.all()
        context['houses'] = houses
        context['house_section'] = house_section
        context['house_floor'] = house_floor
        context['personal_accounts'] = PersonalAccount.objects.filter(flat__isnull=True)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FlatForm(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form, request.POST.get('personal-account'))
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, personal_account_number):
        saved_flat = form.save()
        try:
            personal_account = PersonalAccount.objects.get(flat=saved_flat)
            if personal_account.number != personal_account_number:
                personal_account.flat = None
                personal_account.save()
                if personal_account_number:
                    try:
                        new_personal_account = PersonalAccount.objects.get(number=personal_account_number)
                        new_personal_account.flat = saved_flat
                        new_personal_account.save()
                    except PersonalAccount.DoesNotExist:
                        PersonalAccount.objects.create(number=personal_account_number,
                                                       flat=saved_flat)
        except PersonalAccount.DoesNotExist:
            if personal_account_number:
                try:
                    personal_account = PersonalAccount.objects.get(number=personal_account_number)
                    personal_account.flat = saved_flat
                    personal_account.save()
                except PersonalAccount.DoesNotExist:
                    PersonalAccount.objects.create(number=personal_account_number,
                                                   flat=saved_flat)
        return redirect('flat-detail', flat_pk=saved_flat.pk)


def delete_flat(request, flat_pk):
    try:
        flat_to_delete = Flat.objects.get(pk=flat_pk)
        flat_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except (Flat.DoesNotExist, KeyError, AttributeError, ProtectedError):
        return JsonResponse({'answer': 'failed'})


def flat_number_is_unique(request):
    try:
        Flat.objects.get(number=request.GET.get('number'))
        return JsonResponse({'answer': 'failed'})
    except Flat.DoesNotExist:
        return JsonResponse({'answer': 'success'})


def personal_account_context(context, flats=Flat.objects.none()):
    """Separate function for forming context in both CreateView and UpdateView of PersonalAccount instances"""

    flats = flats
    house_section: dict[
        int, list[list[int, str]]] = {}  # used in frontend for dynamical changing of sections while house was changed
    section_flat: dict[
        int, list[list[int, str]]] = {}  # used in frontend for dynamical changing of flats while section was changed
    houses = []  # used for displaying houses in select tag in frontend

    for flat in flats:
        houses.append(flat.house)
        if not house_section.get(flat.house.id):
            house_section[flat.house.id] = [[flat.section.id, flat.section.name]]
        else:
            if [flat.section.id, flat.section.name] not in house_section[flat.house.id]:
                house_section[flat.house.id].append([flat.section.id, flat.section.name])

        if not section_flat.get(flat.section.id):
            section_flat[flat.section.id] = [[flat.id, flat.number]]
        else:
            section_flat[flat.section.id].append([flat.id, flat.number])

    context['flats'] = flats
    context['house_section'] = house_section
    context['section_flat'] = section_flat
    context['houses'] = set(houses)
    return context


class PersonalAccountCreateView(CreateView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-create-update.html'
    form_class = PersonalAccountForm

    def get_context_data(self, **kwargs):
        context = super(PersonalAccountCreateView, self).get_context_data(**kwargs)
        context = personal_account_context(context, Flat.objects.select_related('personalaccount', 'house', 'section',
                                                                                'owner').filter(
            personalaccount__isnull=True))
        context['create_new'] = {'create': 'true'}
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        account = form.save()
        if account.flat:
            account.status = 'active'
            account.save()
        return redirect('personal-account-detail', account_pk=account.pk)


class PersonalAccountDetailView(DetailView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-detail.html'
    pk_url_kwarg = 'account_pk'

    def get_object(self, queryset=None):
        try:
            personal_account = PersonalAccount.objects.filter(pk=self.kwargs.get('account_pk'))
            return personal_account
        except PersonalAccount.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super(PersonalAccountDetailView, self).get_context_data(**kwargs)
        context.update(calculate_notoriety_and_receipt_sum(self.get_object()))
        context['object'] = context['personal_accounts'][0]
        return context


def calculate_notoriety_and_receipt_sum(personal_accounts: QuerySet):
    """Calculate incomes notoriety's sum and receipt's services sum for each personal account"""

    # making annotation separately in order to avoid multiplied wrong answer
    accounts_with_notoriety_sum = personal_accounts \
        .annotate(rest=Sum(Case(When(notoriety__sum__isnull=True, then=Value(0.00)),
                                default='notoriety__sum',
                                output_field=FloatField()))) \
        .order_by('-id')  # get sum of all notorieties bounded to account number
    accounts_with_receipt_sum = personal_accounts \
        .annotate(receipt_sum=Sum(Case(When(receipt__receiptservices__total_price__isnull=True, then=Value(0.00)),
                                       default='receipt__receiptservices__total_price',
                                       output_field=FloatField()),
                                  filter=(Q(receipt__is_completed=True)))) \
        .order_by('-id')  # get sum of all receipts bounded to account number

    # pass all annotation calculations to main object_list
    personal_accounts = personal_accounts.annotate(
        rest=Subquery(accounts_with_notoriety_sum.filter(pk=OuterRef('id')).values('rest')[:1]),
        receipt_sum=Subquery(accounts_with_receipt_sum.filter(pk=OuterRef('id')).values('receipt_sum')[:1]),
        subtraction=Case(When(rest__isnull=True, then=Value(0.00)), default='rest', output_field=FloatField()) -
                    Case(When(receipt_sum__isnull=True, then=Value(0.00)), default='receipt_sum',
                         output_field=FloatField()))

    return {'personal_accounts': personal_accounts}


def calculate_totals(personal_accounts: QuerySet):
    """Calculating sum of overall cash register, overall sum by all accounts and overall sum of debt by all accounts"""
    # count sum of all notorieties
    checkout_condition = Notoriety.objects.all().values('sum') \
        .aggregate(
        notoriety_income_sum=Sum('sum', filter=Q(type='income'), output_field=FloatField()),
        notoriety_outcome_sum=Sum('sum', filter=Q(type='outcome'),output_field=FloatField()))
    checkout_condition = {
        'sum': (checkout_condition.get('notoriety_income_sum') if checkout_condition.get('notoriety_income_sum') else 0.00)
               - (checkout_condition.get('notoriety_outcome_sum') if checkout_condition.get('notoriety_outcome_sum') else 0.00)
    }

    # count sum by all account's positive rest
    sum_by_account = personal_accounts.aggregate(
        sum=Sum(Case(When(subtraction__lte=0, then=Value(0.0)), default='subtraction', output_field=FloatField())))

    # count debt by all account's negative rest
    debt_by_account = personal_accounts.aggregate(
        debt=-Sum(Case(When(subtraction__gte=0, then=Value(0.0)), default='subtraction', output_field=FloatField())))

    return {'checkout_condition': checkout_condition, 'debt_by_account': debt_by_account,
            'sum_by_account': sum_by_account}


def count_all_totals(personal_accounts: QuerySet):
    """Coalesce calculation of notoriety's and receipt's sum with totals"""
    answer = {}
    answer.update(calculate_notoriety_and_receipt_sum(personal_accounts))
    answer.update(calculate_totals(answer.get('personal_accounts')))
    return answer


class PersonalAccountListView(ListView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-list.html'

    # needed to be finished
    def get_queryset(self):
        return PersonalAccount.objects \
            .select_related('flat', 'flat__section', 'flat__house', 'flat__owner') \
            .prefetch_related('notoriety_set', 'receipt_set', 'receipt_set__receiptservices') \
            .order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PersonalAccountListView, self).get_context_data(object_list=object_list, **kwargs)
        context.update(count_all_totals(context['object_list']))

        return context


class PersonalAccountUpdateView(UpdateView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-create-update.html'
    pk_url_kwarg = 'account_pk'
    form_class = PersonalAccountForm

    def get_object(self, queryset=None):
        try:
            return PersonalAccount.objects.select_related('flat', 'flat__section', 'flat__house').prefetch_related(
                'flat__house__section_set').get(pk=self.kwargs['account_pk'])
        except PersonalAccount.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(PersonalAccountUpdateView, self).get_context_data(**kwargs)
        context = personal_account_context(context, Flat.objects.select_related('personalaccount',
                                                                                'house',
                                                                                'section',
                                                                                'owner').filter(
            personalaccount__isnull=True))

        context['create_new'] = {'create': 'false'}

        # if flat related to current personal account exists
        try:
            # union Queryset<Flat> with flat related to current personal account for displaying it in select tag in frontend
            context['flats'] = context['flats'].union(
                Flat.objects.select_related('personalaccount', 'house', 'section', 'owner').filter(
                    pk=self.object.flat.pk))

            # add current flat to section's list of flats for displaying in frontend
            if context['section_flat'].get(self.object.flat.section.id):
                if [self.object.flat.id, self.object.flat.number] not in context['section_flat'][
                        self.object.flat.section.id]:
                    context['section_flat'][self.object.flat.section.id].append(
                        [self.object.flat.id, self.object.flat.number])
            else:
                context['section_flat'][self.object.flat.section.id] = [[self.object.flat.id, self.object.flat.number]]

            # add section of current personal account's flat to list of sections in separate house
            if self.object.flat.house not in context['houses']:
                context['house_section'][self.object.flat.house.pk] = [
                    [self.object.flat.section.pk, self.object.flat.section.name]]
                context['houses'].add(self.object.flat.house)
        except AttributeError:
            return context

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        account_saved = form.save(commit=False)

        # if flat was deleted from account, it deletes flat from model instance
        if not form.cleaned_data.get('flat'):
            account_saved.flat = None

        # if account is bounded to flat, it cannot be inactive
        if form.cleaned_data.get('flat') and account_saved.status != 'active':
            account_saved.status = 'active'
        account_saved.save()
        return redirect('personal-account-detail', account_pk=account_saved.pk)


def delete_personal_account(request, account_pk):
    try:
        account_to_delete = PersonalAccount.objects.prefetch_related('flat__evidence_set').get(pk=account_pk)
        if account_to_delete.flat.evidence_set.all().count() > 0:
            raise PersonalAccount.DoesNotExist()
        account_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except (PersonalAccount.DoesNotExist, KeyError, AttributeError, ProtectedError):
        return JsonResponse({'answer': 'failed'})


def personal_account_is_unique(request):
    try:
        PersonalAccount.objects.get(number=request.GET.get('number'), flat__isnull=False)
        return JsonResponse({'answer': 'failed'})
    except PersonalAccount.DoesNotExist:
        return JsonResponse({'answer': 'success'})


class OwnerCreateView(CreateView):
    model = User
    template_name = 'administrator_panel/owner-create-update.html'
    form_class = OwnerForm

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        User.objects.create_user(email=form.cleaned_data.get('email'),
                                 password=form.cleaned_data.get('password'),
                                 name=form.cleaned_data.get('name'),
                                 surname=form.cleaned_data.get('surname'),
                                 role=Role.objects.get(role__exact='owner'),
                                 birthday=form.cleaned_data.get('birthday'),
                                 logo=form.cleaned_data.get('logo'),
                                 father=form.cleaned_data.get('father'),
                                 phone=form.cleaned_data.get('phone'),
                                 viber=form.cleaned_data.get('viber'),
                                 owner_id=form.cleaned_data.get('owner_id'),
                                 telegram=form.cleaned_data.get('telegram'),
                                 status=form.cleaned_data.get('status'),
                                 notes=form.cleaned_data.get('notes'))
        return redirect('owners')


class OwnerUpdateView(UpdateView):
    model = User
    template_name = 'administrator_panel/owner-create-update.html'
    form_class = OwnerForm
    pk_url_kwarg = 'owner_pk'

    def get_object(self, queryset=None):
        try:
            return User.objects.select_related('role').get(pk=self.kwargs.get('owner_pk'), role__role='owner')
        except (User.DoesNotExist, KeyError, AttributeError):
            raise Http404()

    def post(self, request, *args, **kwargs):
        owner = self.get_object()
        form = OwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            return self.form_valid(form, owner)
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, owner):
        old_password = owner.password
        owner_saved = form.save()
        if form.cleaned_data.get('password'):
            owner_saved.set_password(form.cleaned_data.get('password'))
            owner_saved.save()
        else:
            owner_saved.password = old_password
            owner_saved.save()
        return redirect('owners')


class OwnerListView(ListView):
    model = User
    queryset = User.objects.prefetch_related('flat_set', 'flat_set__house').filter(role__role='owner').order_by('-id')
    template_name = 'administrator_panel/owner-list.html'


class OwnerDetailView(DetailView):
    model = User
    template_name = 'administrator_panel/owner-detail.html'
    pk_url_kwarg = 'owner_pk'

    def get_object(self, queryset=None):
        try:
            return User.objects.get(pk=self.kwargs['owner_pk'])
        except User.DoesNotExist:
            raise Http404()


def delete_owner(request, owner_pk):
    try:
        user = User.objects.prefetch_related('flat_set__receipt_set', 'flat_set__personalaccount').get(pk=owner_pk)
        if not user.flat_set.all().exists():
            user.delete()
            return JsonResponse({'answer': 'success'})
        return JsonResponse({'answer': 'failed'})
    except User.DoesNotExist:
        return JsonResponse({'answer': 'failed'})


class EvidenceCreateView(CreateView):
    model = Evidence
    template_name = 'administrator_panel/evidence-create-update.html'
    form_class = EvidenceForm

    def get_context_data(self, **kwargs):
        context = super(EvidenceCreateView, self).get_context_data(**kwargs)
        context = personal_account_context(context, Flat.objects.prefetch_related('house', 'section').filter(
            personalaccount__isnull=False))
        context['services'] = Service.objects.select_related('measurement_unit').filter(show_in_counters=True)
        context['create_new_number'] = {'create': 'true'}
        if self.request.GET.get('base_evidence'):
            context['base_evidence'] = Evidence.objects.select_related('flat', 'flat__house', 'flat__section',
                                                                       'service').prefetch_related(
                'flat__house__section_set', 'flat__section__flat_set').get(pk=self.request.GET.get('base_evidence'))
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        evidence_saved = form.save()
        if self.request.POST.get('create-again'):
            return redirect(f"{reverse('evidence-create')}?base_evidence={evidence_saved.pk}")
        return redirect('evidence-detail', evidence_pk=evidence_saved.pk)


class EvidenceDetailView(DetailView):
    model = Evidence
    template_name = 'administrator_panel/evidence-detail.html'
    pk_url_kwarg = 'evidence_pk'


class GroupedEvidenceListView(ListView):
    model = Evidence
    template_name = 'administrator_panel/evidence-grouped-list.html'
    queryset = Evidence.objects.select_related('service',
                                               'flat',
                                               'flat__house',
                                               'flat__section',
                                               'service__measurement_unit').all().annotate(
        distinct_name=Concat('flat', 'service')).distinct('distinct_name')


class ServiceEvidenceListView(ListView):
    model = Evidence
    template_name = 'administrator_panel/evidence-counter-list.html'

    def get_queryset(self):
        flat_pk = self.request.GET.get('flat')
        service_pk = self.request.GET.get('service')
        try:
            return Evidence.objects.select_related('flat', 'service', 'flat__house', 'flat__section',
                                                   'service__measurement_unit').filter(
                flat=Flat.objects.get(pk=flat_pk), service=Service.objects.get(pk=service_pk)).order_by('-id')
        except (Evidence.DoesNotExist, Flat.DoesNotExist, Service.DoesNotExist, KeyError, AttributeError):
            raise Http404()


class EvidenceUpdateView(UpdateView):
    model = Evidence
    template_name = 'administrator_panel/evidence-create-update.html'
    form_class = EvidenceForm
    pk_url_kwarg = 'evidence_pk'

    def get_object(self, queryset=None):
        try:
            return Evidence.objects.select_related('flat',
                                                   'service',
                                                   'flat__house',
                                                   'flat__section',
                                                   'flat__owner').get(pk=self.kwargs.get('evidence_pk'))
        except (Evidence.DoesNotExist, AttributeError, KeyError):
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super(EvidenceUpdateView, self).get_context_data(**kwargs)
        context = personal_account_context(context, Flat.objects.prefetch_related('house', 'section').filter(
            personalaccount__isnull=False))
        context['services'] = Service.objects.select_related('measurement_unit').filter(show_in_counters=True)
        context['create_new_number'] = {'create': 'false'}
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, instance=self.get_object())
        if form.is_valid():
            return self.form_valid(form)
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        evidence_saved = form.save()
        return redirect('evidence-detail', evidence_pk=evidence_saved.pk)


def delete_evidence(request, evidence_pk):
    try:
        evidence_to_delete = Evidence.objects.get(pk=evidence_pk)
        evidence_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except Evidence.DoesNotExist:
        return JsonResponse({'answer': 'failed'})


class ReceiptCreateView(CreateView):
    model = Receipt
    template_name = 'administrator_panel/receipt-create-update.html'
    form_class = ReceiptForm

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        context = personal_account_context(context,
                                           flats=Flat.objects.select_related('house', 'section', 'personalaccount',
                                                                             'tariff', 'owner',
                                                                             'section__house').filter(
                                               personalaccount__isnull=False, personalaccount__status='active'))

        # adding sections of each house, whose flats are with personal account in order to display it on firstly loaded page
        if self.request.GET.get('base_receipt') or self.request.GET.get('flat_id'):
            context['sections_in_houses'] = set()
            for flat in context['flats']:
                context['sections_in_houses'].add(flat.section)

            if self.request.GET.get('flat_id'):
                # trying to get flat, on which new receipt will be based
                try:
                    context['base_flat'] = Flat.objects.select_related('personalaccount',
                                                                       'house',
                                                                       'section',
                                                                       'tariff',
                                                                       'owner').get(pk=self.request.GET.get('flat_id'))
                except Flat.DoesNotExist:
                    raise Http404()

            if self.request.GET.get('base_receipt'):
                # getting receipt basing on which new receipt will be built
                try:
                    context['base_receipt'] = Receipt.objects.select_related('account',
                                                                             'account__flat',
                                                                             'account__flat__house',
                                                                             'account__flat__section',
                                                                             'account__flat__owner').get(
                        pk=self.request.GET.get('base_receipt'))
                    context['base_receipt_services'] = ReceiptService.objects.select_related('service',
                                                                                             'receipt',
                                                                                             'service__measurement_unit').filter(
                        receipt=context['base_receipt'])
                except Receipt.DoesNotExist:
                    raise Http404()

        context['personal_accounts'] = PersonalAccount.objects.select_related('flat', 'flat__owner').filter(
            flat__isnull=False)
        context['receipt_service_formset'] = receipt_service_formset(queryset=ReceiptService.objects.none())
        context['tariffs'] = Tariff.objects.prefetch_related('tariffservice_set',
                                                             'tariffservice_set__service',
                                                             'tariffservice_set__service__measurement_unit').all()
        context['services'] = Service.objects.select_related('measurement_unit').all()
        context['flat_personal_account'] = {}
        context['create_new_number'] = {'create': 'true'}
        context['flat_tariff'] = {}

        # dictionary where flat.pk is key and flat's personal account is value. If no account - 'none'
        for flat in context['flats']:
            context['flat_personal_account'][flat.id] = flat.personalaccount.number
            if flat.tariff:
                context['flat_tariff'][flat.id] = flat.tariff.id
            else:
                context['flat_tariff'][flat.id] = 'none'

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(self.request.POST)
        receipt_formset = receipt_service_formset(request.POST, queryset=ReceiptService.objects.none())
        if form.is_valid() and receipt_formset.is_valid():
            return self.form_valid(form, receipt_formset=receipt_formset)
        self.object = None
        context = self.get_context_data()
        context['form'] = form
        context['receipt_service_formset'] = receipt_formset
        context['create_new_number'] = {'create': 'false'}
        return self.render_to_response(context)

    def form_valid(self, form, receipt_formset):
        receipt_saved = form.save()
        for receipt_service_form in receipt_formset.forms:
            if receipt_service_form.cleaned_data.get('service') and receipt_service_form.cleaned_data.get('amount') \
                    and receipt_service_form.cleaned_data.get('price') and receipt_service_form.cleaned_data.get(
                'total_price'):
                form_saved = receipt_service_form.save(commit=False)
                form_saved.receipt = receipt_saved
                form_saved.save()
        return redirect('receipt-detail', receipt_pk=receipt_saved.pk)


class ReceiptUpdateView(UpdateView):
    model = Receipt
    template_name = 'administrator_panel/receipt-create-update.html'
    pk_url_kwarg = 'receipt_id'
    form_class = ReceiptForm

    def get_object(self, queryset=None):
        try:
            return Receipt.objects.select_related('account',
                                                  'account__flat',
                                                  'account__flat__house',
                                                  'account__flat__section').prefetch_related('receiptservices').get(
                pk=self.kwargs.get('receipt_pk'))
        except Receipt.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(ReceiptUpdateView, self).get_context_data(**kwargs)
        context = personal_account_context(context,
                                           flats=Flat.objects.select_related('house', 'section', 'personalaccount',
                                                                             'tariff', 'owner',
                                                                             'section__house').filter(
                                               personalaccount__isnull=False, personalaccount__status='active'))

        # adding sections of each house, whose flats are with personal account in order to display it on firstly loaded page
        context['sections_in_houses'] = set()
        for flat in context['flats']:
            context['sections_in_houses'].add(flat.section)

        context['personal_accounts'] = PersonalAccount.objects.select_related('flat', 'flat__owner').filter(
            flat__isnull=False)
        context['receipt_service_formset'] = receipt_service_formset(
            queryset=ReceiptService.objects.select_related('service', 'service__measurement_unit').filter(
                receipt=self.object))
        context['tariffs'] = Tariff.objects.prefetch_related('tariffservice_set',
                                                             'tariffservice_set__service',
                                                             'tariffservice_set__service__measurement_unit').all()
        context['services'] = Service.objects.select_related('measurement_unit').all()
        context['flat_personal_account'] = {}
        context['create_new_number'] = {'create': 'false'}
        context['flat_tariff'] = {}

        # dictionary where flat.pk is key and flat's personal account is value. If no account - 'none'
        for flat in context['flats']:
            context['flat_personal_account'][flat.id] = flat.personalaccount.number
            if flat.tariff:
                context['flat_tariff'][flat.id] = flat.tariff.id
            else:
                context['flat_tariff'][flat.id] = 'none'

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, instance=self.object)
        receipt_formset = receipt_service_formset(request.POST,
                                                  queryset=ReceiptService.objects.filter(receipt=self.object))
        if form.is_valid() and receipt_formset.is_valid():
            return self.form_valid(form, receipt_formset=receipt_formset)
        context = self.get_context_data()
        context['form'] = form
        context['receipt_service_formset'] = receipt_formset
        return self.render_to_response(context)

    def form_valid(self, form, receipt_formset):
        receipt_saved = form.save()
        for receipt_service_form in receipt_formset.forms:
            if receipt_service_form.cleaned_data.get('service') and receipt_service_form.cleaned_data.get('amount') \
                    and receipt_service_form.cleaned_data.get('price') and receipt_service_form.cleaned_data.get(
                'total_price'):
                form_saved = receipt_service_form.save(commit=False)
                form_saved.receipt = receipt_saved
                form_saved.save()
        return redirect('receipt-detail', receipt_pk=receipt_saved.pk)


class ReceiptDetailView(DetailView):
    model = Receipt
    template_name = 'administrator_panel/receipt-detail.html'
    pk_url_kwarg = 'receipt_pk'

    def get_object(self, queryset=None):
        try:
            return Receipt.objects.select_related('account',
                                                  'account__flat',
                                                  'account__flat__owner',
                                                  'account__flat__house',
                                                  'account__flat__section') \
                .prefetch_related('receiptservices',
                                  'receiptservices__service',
                                  'receiptservices__service__measurement_unit') \
                .annotate(summ=Sum('receiptservices__total_price')) \
                .get(pk=self.kwargs.get('receipt_pk'))
        except (Receipt.DoesNotExist, KeyError, AttributeError):
            raise Http404()


class ReceiptListView(ListView):
    model = Receipt
    template_name = 'administrator_panel/receipt-list.html'

    def get_queryset(self):
        return Receipt.objects \
            .select_related('account', 'account__flat', 'account__flat__house', 'account__flat__section',
                            'account__flat__owner') \
            .prefetch_related('receiptservices').all().order_by('-id') \
            .annotate(summ=Sum('receiptservices__total_price'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceiptListView, self).get_context_data(object_list=object_list, **kwargs)
        context.update(count_all_totals(PersonalAccount.objects.all()))

        return context


class EvidenceResponse(MultipleObjectMixin, View):
    model = Evidence

    def get_queryset(self):
        try:
            evidences = Evidence.objects.select_related('flat__personalaccount',
                                                        'flat',
                                                        'flat__house',
                                                        'flat__section',
                                                        'service',
                                                        'service_id',
                                                        'service__measurement_unit') \
                .filter(flat__personalaccount__number=self.request.GET.get('account_number')) \
                .values('number',
                        'status',
                        'date_from',
                        'flat__house__name',
                        'flat__section__name',
                        'flat__number',
                        'service__name',
                        'counter_evidence',
                        'service__measurement_unit__name',
                        'service_id')
            return list(evidences)
        except (KeyError, AttributeError):
            return None

    def get_context_data(self, **kwargs):
        evidences = self.get_queryset()
        for evidence in evidences:
            evidence['date_from_formatted'] = evidence['date_from'].strftime('%d.%m.%Y')
            import locale
            locale.setlocale(locale.LC_ALL, 'uk_UA.utf8')
            evidence['date_from_month'] = evidence['date_from'].strftime('%B').title()
        return JsonResponse({'evidences': evidences})

    def get(self, request):
        context = self.get_context_data()
        return context


def receipt_service_delete(request, receipt_service_delete_pk):
    try:
        receipt_service_to_delete = ReceiptService.objects.get(pk=receipt_service_delete_pk)
        receipt_service_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except (ReceiptService.DoesNotExist, KeyError, AttributeError):
        return JsonResponse({'answer': 'failed'})


def delete_receipt(request):
    if request.is_ajax():
        try:
            receipt_to_delete = Receipt.objects.get(pk=request.GET.get('receipt_id'))
            receipt_to_delete.delete()
            return JsonResponse({'answer': 'success'})
        except (Receipt.DoesNotExist, AttributeError, KeyError):
            return JsonResponse({'answer': 'failed'})

    if request.POST.get('receipt_id'):
        try:
            receipt_to_delete = Receipt.objects.get(pk=request.POST.get('receipt_id'))
            receipt_to_delete.delete()
        finally:
            return redirect('receipts')

    if request.POST.get('receipts_to_delete'):
        receipts_pk = request.POST.get('receipts_to_delete').split(',')[:-1]
        try:
            receipts = Receipt.objects.filter(pk__in=receipts_pk)
            receipts.delete()
        finally:
            return redirect('receipts')
    return redirect('receipts')


class NotorietyCreateView(CreateView):
    model = Notoriety
    template_name = 'administrator_panel/notoriety-create-update.html'
    form_class = NotorietyForm

    def get_context_data(self, **kwargs):
        context = super(NotorietyCreateView, self).get_context_data(**kwargs)
        if kwargs.get('type'):
            context['type'] = kwargs.get('type')
        else:
            context['type'] = self.request.GET.get('type') if self.request.GET.get(
                'type') else 'outcome'  # if type is not defined it is set 'outcome'

        # create notoriety based on already existing notoriety
        if self.request.GET.get('base_notoriety'):
            try:
                context['base_notoriety'] = Notoriety.objects \
                    .select_related('manager', 'manager__role', 'account', 'account__flat__owner', 'article') \
                    .get(pk=self.request.GET.get('base_notoriety'))
            except Notoriety.DoesNotExist:
                raise Http404()

        # create notoriety with indicated personal account
        if self.request.GET.get('account'):
            try:
                context['base_account'] = PersonalAccount.objects\
                    .select_related('flat', 'flat__owner')\
                    .get(pk=self.request.GET.get('account'))
                context['type'] = 'income'
            except (PersonalAccount.DoesNotExist, KeyError, AttributeError):
                raise Http404()

        context['personal_accounts'] = PersonalAccount.objects.select_related('flat', 'flat__owner') \
            .filter(flat__isnull=False, status='active', flat__owner__isnull=False)
        context['owners'] = set([account.flat.owner for account in context['personal_accounts']])
        context['articles'] = ArticlePayment.objects.filter(type__exact=context['type'])
        context['managers'] = User.objects.select_related('role').filter(
            role__role__in=['director', 'manager', 'accountant'])

        context['create_new'] = {'create': 'true'}
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        self.object = None
        context = self.get_context_data(type=self.request.POST.get('type'))
        context['form'] = form
        context['create_new'] = {'create': 'false'}
        return self.render_to_response(context)

    def form_valid(self, form):
        notoriety_saved = form.save()
        return redirect('notoriety-detail', notoriety_pk=notoriety_saved.pk)


class NotorietyDetailView(DetailView):
    model = Notoriety
    template_name = 'administrator_panel/notoriety-detail.html'
    pk_url_kwarg = 'notoriety_pk'

    def get_object(self, queryset=None):
        try:
            return Notoriety.objects.select_related('account',
                                                    'account__flat',
                                                    'account__flat__owner',
                                                    'manager',
                                                    'manager__role',
                                                    'article').get(pk=self.kwargs.get('notoriety_pk'))
        except (Notoriety.DoesNotExist, KeyError, AttributeError):
            return None


class NotorietyUpdateView(UpdateView):
    model = Notoriety
    template_name = 'administrator_panel/notoriety-create-update.html'
    pk_url_kwarg = 'notoriety_pk'
    form_class = NotorietyForm

    def get_object(self, queryset=None):
        try:
            return Notoriety.objects \
                .select_related('account', 'account__flat', 'account__flat__owner', 'manager', 'manager__role',
                                'article') \
                .get(pk=self.kwargs.get('notoriety_pk'))
        except (Notoriety.DoesNotExist, KeyError, AttributeError):
            return None

    def get_context_data(self, **kwargs):
        context = super(NotorietyUpdateView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        context['type'] = self.object.type
        context['create_new'] = {'create': 'false'}
        context['personal_accounts'] = PersonalAccount.objects.select_related('flat', 'flat__owner') \
            .filter(flat__isnull=False, status='active', flat__owner__isnull=False)
        context['owners'] = set([account.flat.owner for account in context['personal_accounts']])
        context['articles'] = ArticlePayment.objects.filter(type__exact=context['type'])
        context['managers'] = User.objects.select_related('role').filter(
            role__role__in=['director', 'manager', 'accountant'])
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        notoriety_saved = form.save()
        return redirect('notoriety-detail', notoriety_pk=notoriety_saved.pk)


class NotorietyListView(ListView):
    model = Notoriety
    template_name = 'administrator_panel/notoriety-list.html'
    queryset = Notoriety.objects.select_related('article', 'account', 'account__flat__owner').all().order_by(
        '-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NotorietyListView, self).get_context_data(object_list=object_list, **kwargs)
        context.update(count_all_totals(PersonalAccount.objects.all()))

        return context


class NotorietyDeleteView(SingleObjectMixin, View):
    model = Notoriety
    pk_url_kwarg = 'notoriety_pk'

    def get_queryset(self):
        return Notoriety.objects.all()

    def get_object(self, queryset=None):
        try:
            return queryset.get(pk=self.kwargs.get('notoriety_pk'))
        except (Notoriety.DoesNotExist, KeyError, AttributeError):
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        try:
            self.object.delete()
            if self.request.is_ajax():
                return JsonResponse({'answer': 'success'})
            return redirect('notorieties')
        except (Notoriety.DoesNotExist, KeyError, AttributeError):
            if self.request.is_ajax():
                return JsonResponse({'answer': 'failed'})


class ReceiptTemplateCreateView(CreateView):
    model = Template
    template_name = 'administrator_panel/template-create.html'
    form_class = ReceiptTemplateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Template.objects.all().order_by('id')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('template-create')
        return redirect('template-create')


class TemplateDefault(SingleObjectMixin, View):
    model = Template
    pk_url_kwarg = 'template_pk'

    def get_object(self, queryset=None):
        try:
            return Template.objects.get(pk=self.kwargs.get('template_pk'))
        except Template.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            try:
                another_default = Template.objects.get(is_default=True)
                another_default.is_default = False
                another_default.save()
            except Template.DoesNotExist:
                pass
            obj.is_default = True
            obj.save()
            return redirect('template-create')
        return redirect('template-create')


class TemplateDeleteView(SingleObjectMixin, View):
    model = Template
    pk_url_kwarg = 'template_pk'

    def get_object(self, queryset=None):
        try:
            return Template.objects.get(pk=self.kwargs.get('template_pk'))
        except Template.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            if not obj.is_default:
                obj.delete()
                return JsonResponse({'answer': 'success'})
            return JsonResponse({'answer': 'template is default'})
        return JsonResponse({'answer': 'failed'})


class BuildReceiptFileView(SingleObjectMixin, View):
    model = Receipt

    def get(self, request, *args, **kwargs):
        try:
            template = Template.objects.get(pk=request.GET.get('template')).file

            receipt = Receipt.objects.select_related('account',
                                                     'account__flat',
                                                     'account__flat__owner')\
                .prefetch_related('receiptservices',
                                  'receiptservices__service',
                                  'account__notoriety_set')\
                .filter(pk=request.GET.get('receipt'))
            if receipt.count() == 0:
                raise Receipt.DoesNotExist()

            # get account for calculating the total sum on account
            personal_account = PersonalAccount.objects\
                .select_related('flat', 'flat__section', 'flat__house', 'flat__owner') \
                .prefetch_related('notoriety_set', 'receipt_set', 'receipt_set__receiptservices')\
                .filter(pk=receipt[0].account.pk)
            if personal_account.count() == 0:
                raise PersonalAccount.DoesNotExist()

            personal_account = calculate_notoriety_and_receipt_sum(personal_account)['personal_accounts']
            print(personal_account)
            receipt = receipt.annotate(receipt_sum=Sum('receiptservices__total_price'))

            receipt = receipt[0]
            payment_requisites = ArticlePayment.objects.first()

            wb = openpyxl.Workbook()
            base_template = openpyxl.load_workbook(filename=template.path)
            base_sheet = base_template.active
            ws = wb.create_sheet(f'receipt-№{receipt.number}_{timezone.now().day}.{timezone.now().month}.{timezone.now().year}')

            reserved_words = {
                '%payCompany%': payment_requisites.name if payment_requisites else 'N/A',
                '%accountNumber%': receipt.account.number,
                '%invoiceNumber%': receipt.number,
                '%invoiceDate%': f'{receipt.date_from.day}.{receipt.date_from.month}.{receipt.date_from.year}',
                '%invoiceAddress%': f'{receipt.account.flat.owner.surname} {receipt.account.flat.owner.name} {receipt.account.flat.owner.father}' if receipt.account.flat.owner else 'N\A',
                '%accountBalance%': personal_account[0].subtraction,
                '%total%': receipt.receipt_sum,
                '%invoiceMonth%': f'{receipt.date_from.month} {receipt.date_from.year}',
                '%totalDebt%': abs(personal_account[0].subtraction) if personal_account[0].subtraction < 0 else 0.00,

            }
            for index, row in enumerate(base_sheet):
                for index_second, cell in enumerate(row):
                    val = base_sheet.cell(row=index+1, column=index_second+1).value
                    if val:
                        if val.startswith('%'):
                            ws.cell(row=index+1, column=index_second+1).value = reserved_words.get(val)
                        else:
                            ws.cell(row=index+1, column=index_second+1).value = val
                        print(ws.cell(row=index+1, column=index_second+1).value)
            wb.save(f'{settings.MEDIA_ROOT}/receipts/receipt-№{receipt.number}_{timezone.now().day}.{timezone.now().month}.{timezone.now().year}.xlsx')
            return JsonResponse({'answer': 'okey'})
        except (Template.DoesNotExist, Receipt.DoesNotExist, PersonalAccount.DoesNotExist):
            return JsonResponse({'answer': 'failed'})
