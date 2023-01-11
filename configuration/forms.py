from django.forms import modelformset_factory, ModelForm, CharField, ModelChoiceField, FloatField, BooleanField
from django.forms.widgets import TextInput, CheckboxInput

from .models import *


def measurement_unit_formset(has_queryset):
    formset = modelformset_factory(MeasurementUnit,
                                   form=MeasurementUnitForm,
                                   extra=(0 if has_queryset else 1))
    return formset


def service_formset(has_queryset):
    formset = modelformset_factory(Service,
                                   form=ServiceForm,
                                   extra=(0 if has_queryset else 1))
    return formset


class MeasurementUnitForm(ModelForm):
    name = CharField(required=False)

    class Meta:
        model = MeasurementUnit
        exclude = ('is_used',)

    def clean(self, *args, **kwargs):
        cleaned_data = super(MeasurementUnitForm, self).clean()
        self._errors = {}

        return cleaned_data


class ServiceForm(ModelForm):
    name = CharField(required=False)
    measurement_unit = ModelChoiceField(required=False, queryset=MeasurementUnit.objects.all())

    class Meta:
        model = Service
        exclude = ('is_used',)

    def clean(self, *args, **kwargs):
        cleaned_data = super(ServiceForm, self).clean()
        self._errors = {}

        return cleaned_data


class TariffForm(ModelForm):

    class Meta:
        model = Tariff
        exclude = ('currency', 'service_tariff')

    def clean(self):
        cleaned_data = super(TariffForm, self).clean()
        self._errors = {}

        return cleaned_data


class TariffServiceForm(ModelForm):
    tariff = ModelChoiceField(required=False, queryset=Tariff.objects.all())
    service = ModelChoiceField(required=False, queryset=Service.objects.all())
    price = FloatField(required=False)

    class Meta:
        model = TariffService
        exclude = ('currency',)

    def clean(self):
        cleaned_data = super(TariffServiceForm, self).clean()
        self._errors = {}

        return cleaned_data


tariff_service_formset = modelformset_factory(TariffService,
                                              form=TariffServiceForm,
                                              extra=0)


role_formset = modelformset_factory(Role,
                                    exclude=('role',),
                                    extra=0)


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('name', 'surname', 'phone', 'email', 'password', 'role', 'status')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        if self.instance:
            self._errors = {}

        return cleaned_data


class PaymentRequisitesForm(ModelForm):

    class Meta:
        model = PaymentRequisite
        fields = '__all__'


class ArticlePaymentForm(ModelForm):

    class Meta:
        model = ArticlePayment
        fields = '__all__'


class UserLoginForm(ModelForm):
    remember_me = BooleanField(widget=CheckboxInput(), required=False)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        self._errors = {}
        if not cleaned_data.get('email'):
            self._errors['email'] = 'Поле не може бути пустим'

        if not cleaned_data.get('password'):
            self._errors['password'] = 'Поле не може бути пустим'

        print(self._errors)

        return cleaned_data

    def clean_email(self):
        if not self.cleaned_data.get('email'):
            self._errors['email'] = 'Поле не може бути пустим'
        return self.cleaned_data.get('email')


class UserSelfRegistrationForm(ModelForm):

    class Meta:
        model = User
        fields = ('surname', 'name', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_email(self):
        obj = User.objects.filter(email=self.cleaned_data.get('email')).exclude(id=self.instance.id)
        if obj:
            self._errors['email'] = 'E-mail повинен бути унікальним'
        return self.cleaned_data.get('email')
