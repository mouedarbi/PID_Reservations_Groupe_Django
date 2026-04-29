from django import forms
from catalogue.models import Representation

class RepresentationForm(forms.ModelForm):
    class Meta:
        model = Representation
        fields = ['show', 'schedule', 'location', 'available_seats']
        widgets = {
            'schedule': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # S'assurer que le format est correct pour l'affichage initial lors de l'édition
        if self.instance and self.instance.schedule:
            self.initial['schedule'] = self.instance.schedule.strftime('%Y-%m-%dT%H:%M')
