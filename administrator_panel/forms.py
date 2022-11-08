from django.db.models import Q
from django.forms import BaseModelFormSet, ModelForm, modelformset_factory, ModelChoiceField, CharField, DateField

from phonenumber_field.formfields import PhoneNumberField

from configuration.models import User
from .models import House, HouseUser, Section, Floor, PersonalAccount, Flat, Receipt


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
