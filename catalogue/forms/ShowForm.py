from django.forms import ModelForm
from catalogue.models import Show

class ShowForm(ModelForm):
    class Meta:
        model = Show
        fields = ['slug', 'title', 'description', 'poster_url', 'duration', 'created_in', 'location', 'bookable']
