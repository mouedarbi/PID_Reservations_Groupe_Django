from django import forms
from catalogue.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['show', 'review', 'stars']
        labels = {
            'review': 'Votre avis / critique',
            'stars': 'Note',
        }
        widgets = {
            'show': forms.HiddenInput(),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 15px;', 'placeholder': 'Partagez votre expérience sur ce spectacle...'}),
            'stars': forms.HiddenInput(attrs={'id': 'id_stars_value'}),
        }
