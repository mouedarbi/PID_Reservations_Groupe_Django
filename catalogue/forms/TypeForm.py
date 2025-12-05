from django.forms import ModelForm
from catalogue.models import Type

class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['type']
