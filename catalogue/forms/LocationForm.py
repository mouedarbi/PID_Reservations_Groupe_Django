from django.forms import ModelForm
from catalogue.models import Location

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = [
            'slug', 
            'designation_fr', 'designation_en', 'designation_nl', 
            'address_fr', 'address_en', 'address_nl', 
            'locality', 'website', 'phone'
        ]
