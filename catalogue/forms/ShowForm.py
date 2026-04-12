from django.forms import ModelForm, Textarea
from catalogue.models import Show

class ShowForm(ModelForm):
    class Meta:
        model = Show
        fields = [
            'slug', 
            'title_fr', 'title_en', 'title_nl', 
            'description_fr', 'description_en', 'description_nl', 
            'poster_url', 'duration', 'created_in', 
            'location', 'bookable'
        ]
        widgets = {
            'description_fr': Textarea(attrs={'rows': 4}),
            'description_en': Textarea(attrs={'rows': 4}),
            'description_nl': Textarea(attrs={'rows': 4}),
        }
