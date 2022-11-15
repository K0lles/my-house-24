from django.db.models import Q, Count
from django.db.models.functions import Concat
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models.deletion import ProtectedError

from configuration.models import Role, Tariff, Service, MeasurementUnit
from .forms import *


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
        house = form.save()     # is used for selecting foreign key of new form in formsets

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
        house = form.save()     # is used for selecting foreign key of new form in formsets

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
                                                                                         'house__section_set').get(pk=self.request.GET.get('prev_flat'))
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
                    account.save()
            except PersonalAccount.DoesNotExist:
                PersonalAccount.objects.create(number=personal_account_number,
                                               flat=created_flat)
        print(self.request.POST.get('create-again') == 'create-new')
        if self.request.POST.get('create-again') == 'create-new':
            return redirect(f'{reverse("flat-create")}?prev_flat={created_flat.pk}')
        return redirect('flat-detail', flat_pk=created_flat.pk)


class FlatDetailView(DetailView):
    model = Flat
    template_name = 'administrator_panel/flat-detail.html'
    pk_url_kwarg = 'flat_pk'

    def get_object(self, queryset=None):
        try:
            return Flat.objects.select_related('house', 'section', 'floor', 'owner', 'personalaccount').get(pk=self.kwargs['flat_pk'])
        except Flat.DoesNotExist:
            raise Http404()


class FlatListView(ListView):
    model = Flat
    template_name = 'administrator_panel/flat-list.html'
    queryset = Flat.objects.select_related('house', 'section', 'floor', 'owner', 'personalaccount').all().order_by('-id')


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
    except Flat.DoesNotExist:
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
    house_section: dict[int, list[list[int, str]]] = {}  # used in frontend for dynamical changing of sections while house was changed
    section_flat: dict[int, list[list[int, str]]] = {}   # used in frontend for dynamical changing of flats while sectin was changed
    houses = []     # used for displaying houses in select tag in frontend

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
        context = personal_account_context(context, Flat.objects.select_related('personalaccount', 'house', 'section', 'owner').filter(personalaccount__isnull=True))
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
        if not account.flat:
            account.status = 'inactive'
            account.save()
        return redirect('flats')


class PersonalAccountDetailView(DetailView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-detail.html'
    pk_url_kwarg = 'account_pk'

    def get_object(self, queryset=None):
        try:
            return PersonalAccount.objects.select_related('flat__house',
                                                          'flat__section',
                                                          'flat', 'flat__owner').get(pk=self.kwargs['account_pk'])
        except PersonalAccount.DoesNotExist:
            raise Http404()


class PersonalAccountListView(ListView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-list.html'
    queryset = PersonalAccount.objects.select_related('flat',
                                                      'flat__section',
                                                      'flat__house',
                                                      'flat__owner').all().order_by('-id')


class PersonalAccountUpdateView(UpdateView):
    model = PersonalAccount
    template_name = 'administrator_panel/personal_account-create-update.html'
    pk_url_kwarg = 'account_pk'
    form_class = PersonalAccountForm

    def get_object(self, queryset=None):
        try:
            return PersonalAccount.objects.select_related('flat', 'flat__section', 'flat__house').prefetch_related('flat__house__section_set').get(pk=self.kwargs['account_pk'])
        except PersonalAccount.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(PersonalAccountUpdateView, self).get_context_data(**kwargs)
        context = personal_account_context(context, Flat.objects.select_related('personalaccount', 'house', 'section', 'owner').filter(personalaccount__isnull=True))

        # if flat related to current personal account exists
        try:
            # union Queryset<Flat> with flat related to current personal account for displaying it in select tag in frontend
            context['flats'] = context['flats'].union(
                Flat.objects.select_related('personalaccount', 'house', 'section', 'owner').filter(
                    pk=self.object.flat.pk))

            # add current flat to section's list of flats for displaying in frontend
            if context['section_flat'].get(self.object.flat.section.id):
                if [self.object.flat.id, self.object.flat.number] not in context['section_flat'][self.object.flat.section.id]:
                    context['section_flat'][self.object.flat.section.id].append([self.object.flat.id, self.object.flat.number])
            else:
                context['section_flat'][self.object.flat.section.id] = [[self.object.flat.id, self.object.flat.number]]

            # add section of current personal account's flat to list of sections in separate house
            if self.object.flat.house not in context['houses']:
                context['house_section'][self.object.flat.house.pk] = [[self.object.flat.section.pk, self.object.flat.section.name]]
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
        if not form.cleaned_data.get('flat'):
            account_saved.flat = None
        account_saved.save()
        return redirect('flats')


def delete_personal_account(request, account_pk):
    try:
        account_to_delete = PersonalAccount.objects.get(pk=account_pk)
        account_to_delete.delete()
        return JsonResponse({'answer': 'success'})
    except PersonalAccount.DoesNotExist:
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
        context = personal_account_context(context, Flat.objects.prefetch_related('house', 'section').filter(personalaccount__isnull=False))
        context['services'] = Service.objects.select_related('measurement_unit').filter(show_in_counters=True)
        context['create_new_number'] = {'create': 'true'}
        if self.request.GET.get('base_evidence'):
            context['base_evidence'] = Evidence.objects.select_related('flat', 'flat__house', 'flat__section', 'service').prefetch_related('flat__house__section_set', 'flat__section__flat_set').get(pk=self.request.GET.get('base_evidence'))
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
                                               'service__measurement_unit').all().annotate(distinct_name=Concat('flat', 'service')).distinct('distinct_name')


class ServiceEvidenceListView(ListView):
    model = Evidence
    template_name = 'administrator_panel/evidence-counter-list.html'

    def get_queryset(self):
        flat_pk = self.request.GET.get('flat')
        service_pk = self.request.GET.get('service')
        try:
            return Evidence.objects.select_related('flat', 'service', 'flat__house', 'flat__section', 'service__measurement_unit').filter(flat=Flat.objects.get(pk=flat_pk), service=Service.objects.get(pk=service_pk)).order_by('-id')
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
    template_name = 'administrator_panel/receipt-create.html'
    form_class = ReceiptForm

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        context = personal_account_context(context, flats=Flat.objects.select_related('house', 'section', 'personalaccount', 'tariff').filter(personalaccount__isnull=False, personalaccount__status='active'))
        context['personal_accounts'] = PersonalAccount.objects.select_related('flat', 'flat__owner').filter(flat__isnull=False)
        context['receipt_service_formset'] = receipt_service_formset(queryset=ReceiptService.objects.none())
        context['tariffs'] = Tariff.objects.all()
        context['services'] = Service.objects.select_related('measurement_unit').all()
        context['measurement_units'] = MeasurementUnit.objects.all()
        context['flat_personal_account'] = {}
        context['flat_tariff'] = {}

        for flat in context['flats']:
            context['flat_personal_account'][flat.id] = flat.personalaccount.number
            if flat.tariff:
                context['flat_tariff'][flat.id] = flat.tariff.id
            else:
                context['flat_tariff'][flat.id] = 'none'

        return context

