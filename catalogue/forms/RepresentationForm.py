from django.forms import ModelForm
from catalogue.models import Representation

class RepresentationForm(ModelForm):
    class Meta:
        model = Representation
        fields = ['show', 'schedule', 'location']
