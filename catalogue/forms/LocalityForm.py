from django.forms import ModelForm
from catalogue.models import Locality

class LocalityForm(ModelForm):
    class Meta:
        model = Locality
        fields = ['postal_code', 'locality_fr', 'locality_en', 'locality_nl']
