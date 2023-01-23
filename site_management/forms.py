from django.forms import ModelForm, modelformset_factory, BaseModelFormSet, ImageField

from .models import *


class SeoForm(ModelForm):

    class Meta:
        model = Seo
        fields = '__all__'


class MainPageForm(ModelForm):

    class Meta:
        model = MainPage
        fields = '__all__'


class AboutUsForm(ModelForm):

    class Meta:
        model = AboutUs
        exclude =['gallery', 'additional_gallery']


class DocumentForm(ModelForm):

    class Meta:
        model = Document
        exclude = ['about_us']

    def clean(self):
        cleaned_data = super().clean()
        self._errors = {}
        return cleaned_data


class DocumentModelFormSet(BaseModelFormSet):

    def clean(self):
        super().clean()
        self._errors = {}
        for form in self.forms:
            form._errors = {}


document_formset_factory = modelformset_factory(Document, form=DocumentForm, formset=DocumentModelFormSet, extra=0)


class PhotoForm(ModelForm):
    photo = ImageField(required=False)

    class Meta:
        model = Photo
        exclude = ['gallery']

    def clean(self):
        cleaned_data = super().clean()
        self._errors = {}
        return cleaned_data


class ServiceFrontForm(ModelForm):

    class Meta:
        model = ServiceFront
        fields = '__all__'


class ServiceFrontObjectForm(ModelForm):

    class Meta:
        model = ServiceObjectFront
        exclude = ['service_front']

    def clean(self):
        cleaned_data = super().clean()
        if self._errors.get('photo'):
            del self._errors['photo']
        if self._errors.get('title'):
            del self._errors['title']
        if self._errors.get('description'):
            del self._errors['description']
        return cleaned_data


service_object_front_formset_factory = modelformset_factory(ServiceObjectFront, form=ServiceFrontObjectForm, extra=0)


class TariffPageForm(ModelForm):

    class Meta:
        model = TariffPage
        fields = '__all__'


class TariffObjectFrontForm(ModelForm):

    class Meta:
        model = TariffObjectFront
        exclude = ['tariff_page']


tariff_object_front_formset_factory = modelformset_factory(TariffObjectFront, form=TariffObjectFrontForm, extra=0)
