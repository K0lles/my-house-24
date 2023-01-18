from django.forms import ModelForm, modelformset_factory

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


document_formset_factory = modelformset_factory(Document, DocumentForm, extra=0, can_delete=True)


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = ['gallery']
