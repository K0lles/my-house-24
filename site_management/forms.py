from django.forms import ModelForm

from additional.models import Seo
from .models import *


class MainPageForm(ModelForm):

    class Meta:
        model = MainPage
        fields = '__all__'


class SeoForm(ModelForm):

    class Meta:
        model = Seo
        fields = '__all__'
