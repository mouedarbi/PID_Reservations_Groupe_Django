from django import forms
from catalogue.models import ProducerRequest
from django.utils.translation import gettext_lazy as _

class ProducerRequestForm(forms.ModelForm):
    class Meta:
        model = ProducerRequest
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'presentation', 'motivation']
        labels = {
            'first_name': _("Prénom"),
            'last_name': _("Nom"),
            'email': _("Email"),
            'phone': _("Téléphone"),
            'address': _("Adresse"),
            'presentation': _("Présentez-vous"),
            'motivation': _("Votre motivation"),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'presentation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 500, 'placeholder': _("Présentez-vous brièvement (max 500 caractères)...")}),
            'motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _("Qu'avez-vous l'intention de proposer ?")}),
        }
