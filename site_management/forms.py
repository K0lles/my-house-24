from django.forms import ModelForm, modelformset_factory, BaseModelFormSet

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
        fields = '__all__'


class DocumentForm(ModelForm):

    class Meta:
        model = Document
        exclude = ['about_us']

    def clean(self):
        cleaned_data = super().clean()
        self._errors = {}
        print(f'cleaned data in document: {self.cleaned_data}')
        return cleaned_data


class DocumentModelFormSet(BaseModelFormSet):

    def clean(self):
        super().clean()
        self._errors = {}
        for form in self.forms:
            form._errors = {}


document_formset_factory = modelformset_factory(Document, form=DocumentForm, formset=DocumentModelFormSet, extra=0)


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = ['gallery']

    def clean(self):
        cleaned_data = super().clean()
        if self._errors.get('photo'):
            del self._errors['photo']
        self._errors = {}
        print(f'cleaned data in photo: {self.cleaned_data}')
        print(f'in form with prefix: {self.prefix} there are {self._errors}, photo: {self.cleaned_data.get("photo")}')
        print(self._errors.get('photo'))
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
        self._errors = {}
        print(self.cleaned_data)
        return cleaned_data


service_object_front_formset_factory = modelformset_factory(ServiceObjectFront, form=ServiceFrontObjectForm, extra=0)
