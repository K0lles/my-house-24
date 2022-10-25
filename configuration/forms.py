from django.forms import modelformset_factory, ModelForm, CharField, ModelChoiceField, FloatField
from django.forms.widgets import TextInput

from .models import MeasurementUnit, Service, Tariff, TariffService, Role, PaymentRequisite, ArticlePayment, User


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
        fields = '__all__'

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


class PaymentRequisitesForm(ModelForm):

    class Meta:
        model = PaymentRequisite
        fields = '__all__'


class ArticlePaymentForm(ModelForm):

    class Meta:
        model = ArticlePayment
        fields = '__all__'
