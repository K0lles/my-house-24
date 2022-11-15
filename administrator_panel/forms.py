from django.forms import ModelForm, modelformset_factory, ModelChoiceField, CharField, DateField
from django.utils import timezone

from phonenumber_field.formfields import PhoneNumberField

from configuration.models import User
from .models import House, HouseUser, Section, Floor, PersonalAccount, Flat, Evidence, Receipt, ReceiptService


class HouseForm(ModelForm):

    class Meta:
        model = House
        exclude = ('house_user',)

    def clean(self):
        cleaned_data = super(HouseForm, self).clean()
        self._errors = {}

        return cleaned_data


class HouseUserForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.select_related('role').all(), required=False)

    class Meta:
        model = HouseUser
        exclude = ('house',)

    def clean(self):
        cleaned_data = super(HouseUserForm, self).clean()
        self._errors = {}

        return cleaned_data


house_user_formset = modelformset_factory(HouseUser,
                                          form=HouseUserForm,
                                          extra=0)


class SectionForm(ModelForm):
    name = CharField(required=False)

    class Meta:
        model = Section
        exclude = ('house',)

    def clean(self):
        cleaned_data = super(SectionForm, self).clean()
        self._errors = {}

        return cleaned_data


section_formset = modelformset_factory(Section,
                                       form=SectionForm,
                                       extra=0)


class FloorForm(ModelForm):
    name = CharField(required=False)

    class Meta:
        model = Floor
        exclude = ('house',)

    def clean(self):
        cleaned_data = super(FloorForm, self).clean()
        self._errors = {}

        return cleaned_data


floor_formset = modelformset_factory(Floor,
                                     form=FloorForm,
                                     extra=0)


class FlatForm(ModelForm):

    class Meta:
        model = Flat
        fields = '__all__'

    def clean(self):
        cleaned_data = super(FlatForm, self).clean()
        self._errors = {}

        if not cleaned_data.get('number'):
            self.add_error('number', 'Поле не може бути пустим')
            return cleaned_data

        try:
            flats = Flat.objects.filter(number=cleaned_data.get('number'), house__floor=cleaned_data.get('floor'), house__section=cleaned_data.get('section'))

            # check if other flats in indicated house and in indicated floor do not have same number
            if (not self.instance.pk and flats.count() == 0) or flats.count() == 0:
                raise Flat.DoesNotExist()

            # while updating check if other flats in indicated house and in indicated floor do not have same number
            if self.instance.pk and flats.count() == 1 and flats[0].pk == self.instance.pk:
                raise Flat.DoesNotExist()

            self.add_error('number', 'Квартира із таким номером вже існує на заданому поверсі в заданому секторі')
        except (Flat.DoesNotExist, AttributeError):
            return cleaned_data
        finally:
            return cleaned_data


class PersonalAccountForm(ModelForm):

    class Meta:
        model = PersonalAccount
        fields = '__all__'

    def clean(self):
        cleaned_data = super(PersonalAccountForm, self).clean()
        self._errors = {}
        if cleaned_data.get('number') and not self.instance.pk:
            try:
                PersonalAccount.objects.get(number=cleaned_data.get('number'))
                self.add_error('number', 'Поле не може бути пустим')
            except PersonalAccount.DoesNotExist:
                return cleaned_data

        return cleaned_data


class OwnerForm(ModelForm):
    birthday = DateField(input_formats=['%d.%m.%Y'], required=False)
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        exclude = ('role', 'is_active', 'is_admin')

    def clean(self):
        cleaned_data = super(OwnerForm, self).clean()
        self._errors = {}

        if not cleaned_data.get('name'):
            self._errors['name'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('surname'):
            self._errors['surname'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('owner_id'):
            self._errors['owner_id'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('email'):
            self._errors['email'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('password') and not self.instance.pk:
            self._errors['password'] = 'Це поле не може бути пустим'

        try:
            if (not self.instance.pk and cleaned_data.get('email') and User.objects.get(email=cleaned_data.get('email'))) \
                    or User.objects.filter(email=cleaned_data.get('email')).count() > 1:
                self._errors['email'] = 'Власник з таким email вже існує'
        except User.DoesNotExist:
            return cleaned_data

        return cleaned_data


class EvidenceForm(ModelForm):
    date_from = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())

    def __init__(self, *args, **kwargs):
        super(EvidenceForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices[0] = ('', 'Вибрати...')

    class Meta:
        model = Evidence
        fields = '__all__'

    def clean(self):
        cleaned_data = super(EvidenceForm, self).clean()

        self._errors = {}

        if self.instance.pk:
            got_evidence = Evidence.objects.filter(number=cleaned_data.get('number'))
            if got_evidence.count() != 0 and (got_evidence[0].pk != self.instance.pk and got_evidence.count() == 1):
                self._errors['number'] = 'Рахунок з даним номером вже існує'

        elif not self.instance.pk:
            try:
                Evidence.objects.get(number=cleaned_data.get('number'))
                self._errors['number'] = 'Рахунок з даним номером вже існує'
            except Evidence.DoesNotExist:
                pass

        if not cleaned_data.get('number'):
            self._errors['number'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('flat'):
            self._errors['flat'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('service'):
            self._errors['service'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('status'):
            self._errors['status'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('counter_evidence'):
            self._errors['counter_evidence'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('date_from'):
            self._errors['date_from'] = 'Це поле не може бути пустим'

        return cleaned_data


class ReceiptForm(ModelForm):

    class Meta:
        model = Receipt
        fields = '__all__'


class ReceiptServiceForm(ModelForm):
    receipt = ModelChoiceField(required=False, queryset=Receipt.objects.all())

    class Meta:
        model = ReceiptService
        fields = '__all__'


receipt_service_formset = modelformset_factory(ReceiptService,
                                               form=ReceiptServiceForm,
                                               extra=0)
