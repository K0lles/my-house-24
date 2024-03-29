from django.forms import ModelForm, modelformset_factory, ModelChoiceField, CharField, DateField, BooleanField, \
    ChoiceField, EmailField, Select, Form
from django.utils import timezone
import datetime

from phonenumber_field.formfields import PhoneNumberField

from configuration.models import User, Service
from .models import House, HouseUser, Section, Floor, PersonalAccount, Flat, Evidence, Receipt, ReceiptService, \
    Notoriety, Template, Message, Application


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
    date_to = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())
    date_from = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())
    created_at = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())
    account = CharField(max_length=255)

    class Meta:
        model = Receipt
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ReceiptForm, self).clean()
        self._errors = {}

        if self.instance.pk:
            got_receipt = Receipt.objects.filter(number=cleaned_data.get('number'))
            if got_receipt.count() != 0 and (got_receipt[0].pk != self.instance.pk and got_receipt.count() == 1):
                self._errors['number'] = 'Квитанція з вказаним номером вже існує'

        elif not self.instance.pk:
            try:
                Receipt.objects.get(number=cleaned_data.get('number'))
                self._errors['number'] = 'Квитанція з вказаним номером вже існує'
            except Receipt.DoesNotExist:
                pass

        try:
            cleaned_data['account'] = PersonalAccount.objects.get(number=cleaned_data.get('account'))
        except PersonalAccount.DoesNotExist:
            self._errors['account'] = 'Перевірте правильність'

        return cleaned_data


class ReceiptServiceForm(ModelForm):
    receipt = ModelChoiceField(required=False, queryset=Receipt.objects.all())
    service = ModelChoiceField(required=False, queryset=Service.objects.all())

    class Meta:
        model = ReceiptService
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ReceiptServiceForm, self).clean()
        self._errors = {}

        return cleaned_data


receipt_service_formset = modelformset_factory(ReceiptService,
                                               form=ReceiptServiceForm,
                                               extra=0)


class NotorietyForm(ModelForm):
    created_at = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())

    class Meta:
        model = Notoriety
        fields = '__all__'

    def clean(self):
        cleaned_data = super(NotorietyForm, self).clean()

        if self.instance.pk:
            got_notoriety = Notoriety.objects.filter(number=cleaned_data.get('number'))
            if got_notoriety.count() != 0 and (got_notoriety[0].pk != self.instance.pk and got_notoriety.count() == 1):
                self._errors['number'] = 'Відомість з вказаним номером вже існує'

        elif not self.instance.pk:
            try:
                Notoriety.objects.get(number=cleaned_data.get('number'))
                self._errors['number'] = 'Відомість з вказаним номером вже існує'
            except Notoriety.DoesNotExist:
                pass

        if not cleaned_data.get('sum') or cleaned_data.get('sum') < 0:
            self._errors['sum'] = 'Неправильно вказана ціна'

        if not cleaned_data.get('type') or cleaned_data.get('type') not in ['income', 'outcome']:
            self._errors['type'] = 'Сталася помилка'

        return cleaned_data


class ReceiptTemplateForm(ModelForm):

    class Meta:
        model = Template
        exclude = ('is_default',)


class MessageForm(ModelForm):
    sender = ModelChoiceField(queryset=User.objects.all(), required=False)
    section = ModelChoiceField(queryset=Section.objects.all(), required=False)
    floor = ModelChoiceField(queryset=Floor.objects.all(), required=False)
    flat = ModelChoiceField(queryset=Flat.objects.all(), required=False)
    send_all_debtors = BooleanField(required=False)

    class Meta:
        model = Message
        exclude = ('sender', 'to_specific_owner')

    def clean(self):
        cleaned_data = super().clean()

        self._errors = {}

        if not cleaned_data.get('theme'):
            self._errors['theme'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('main_text'):
            self._errors['main_text'] = 'Це поле не може бути пустим'

        return cleaned_data


class MessageToOwnerForm(ModelForm):
    sender = ModelChoiceField(queryset=User.objects.all(), required=False)
    owner_receiver = ModelChoiceField(queryset=User.objects.select_related('role').filter(role__role='owner'))

    class Meta:
        model = Message
        exclude = ('sender',)

    def clean(self):
        cleaned_data = super().clean()

        self._errors = {}

        if not cleaned_data.get('owner_receiver'):
            self._errors['owner_receiver'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('theme'):
            self._errors['theme'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('main_text'):
            self._errors['main_text'] = 'Це поле не може бути пустим'

        return cleaned_data


class ApplicationForm(ModelForm):
    master_type = ChoiceField(choices=Application.MasterTypeChoices.choices, required=False)
    desired_date = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())

    class Meta:
        model = Application
        exclude = ['created_by_director']


class ApplicationOwnerForm(ModelForm):
    master_type = ChoiceField(choices=Application.MasterTypeChoices.choices, required=False)
    desired_date = DateField(input_formats=['%d.%m.%Y'], initial=timezone.now())
    status = ChoiceField(choices=Application.StatusChoices.choices, required=False)

    class Meta:
        model = Application
        exclude = ['created_by_director']


class OwnerProfileForm(ModelForm):
    birthday = DateField(input_formats=['%d.%m.%Y'], required=False)
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        exclude = ['status', 'owner_id', 'role', 'is_active', 'is_admin', 'created_at']

    def clean(self):
        cleaned_data = super(OwnerProfileForm, self).clean()
        self._errors = {}

        if not cleaned_data.get('name'):
            self._errors['name'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('surname'):
            self._errors['surname'] = 'Це поле не може бути пустим'

        if not cleaned_data.get('email'):
            self._errors['email'] = 'Це поле не може бути пустим'

        try:
            if cleaned_data.get('email') != self.instance.email and User.objects.get(email=cleaned_data.get('email')):
                self._errors['email'] = 'Власник з таким email вже існує'
        except User.DoesNotExist:
            return cleaned_data

        return cleaned_data


class SendInvitationForm(Form):
    email = EmailField()
    phone = CharField()


class AdministrationProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['surname', 'name', 'phone', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if self._errors.get('password'):
            del self._errors['password']
        return cleaned_data

    def clean_email(self):
        obj = User.objects.filter(email=self.cleaned_data.get('email')).exclude(id=self.instance.id)
        if obj:
            self._errors['email'] = 'E-mail повинен бути унікальним'
        return self.cleaned_data.get('email')
