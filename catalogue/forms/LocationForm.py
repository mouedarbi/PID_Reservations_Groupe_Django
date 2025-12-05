from django.forms import ModelForm
from catalogue.models import Location

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['slug', 'designation', 'address', 'locality', 'website', 'phone']
