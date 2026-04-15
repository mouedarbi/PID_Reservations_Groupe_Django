from django import forms
from ..models import ArtistType

class ArtistTypeForm(forms.ModelForm):
    class Meta:
        model = ArtistType
        fields = ['artist', 'type']
        widgets = {
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
