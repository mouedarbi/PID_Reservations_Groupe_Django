from django import forms
from catalogue.models import CriticRequest

class CriticRequestForm(forms.ModelForm):
    class Meta:
        model = CriticRequest
        fields = ['first_name', 'last_name', 'profession', 'media_name', 'website', 'motivation']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre profession actuelle'}),
            'media_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du média / journal'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Lien vers votre site ou portfolio (optionnel)'}),
            'motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Pourquoi souhaitez-vous devenir critique pour ThéâtrePlus ?'}),
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'profession': 'Profession',
            'media_name': 'Média / Journal',
            'website': 'Site Web / Portfolio',
            'motivation': 'Vos motivations',
        }
