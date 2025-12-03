from django import forms
from catalogue.models import Artist

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'firstname',
            'lastname',
        ]
