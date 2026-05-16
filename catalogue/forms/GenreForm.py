from django import forms
from catalogue.models import Genre

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'name_fr', 'name_en', 'name_nl']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border-border bg-input focus:ring-primary w-full rounded-md border py-2 px-4 transition-colors duration-200 focus:ring-2 focus:outline-none'}),
            'name_fr': forms.TextInput(attrs={'class': 'border-border bg-input focus:ring-primary w-full rounded-md border py-2 px-4 transition-colors duration-200 focus:ring-2 focus:outline-none'}),
            'name_en': forms.TextInput(attrs={'class': 'border-border bg-input focus:ring-primary w-full rounded-md border py-2 px-4 transition-colors duration-200 focus:ring-2 focus:outline-none'}),
            'name_nl': forms.TextInput(attrs={'class': 'border-border bg-input focus:ring-primary w-full rounded-md border py-2 px-4 transition-colors duration-200 focus:ring-2 focus:outline-none'}),
        }
