from django.db.models import Q
from django.forms import BaseModelFormSet, ModelForm, modelformset_factory, ModelChoiceField, CharField

from configuration.models import User
from .models import House, HouseUser, Section, Floor, PersonalAccount, Flat


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
            Flat.objects.get(number=cleaned_data.get('number'), house__flat=cleaned_data.get('flat'), house__section=cleaned_data.get('section'))
            self.add_error('number', 'Квартира із таким номером вже існує на даному поверсі')
            return cleaned_data
        except Flat.DoesNotExist:
            return cleaned_data


class PersonalAccountForm(ModelForm):

    class Meta:
        model = PersonalAccount
        fields = '__all__'
