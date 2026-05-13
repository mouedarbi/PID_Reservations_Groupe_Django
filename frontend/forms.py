from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Nom"),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('Votre nom complet'), 'class': 'form-input'})
    )
    email = forms.EmailField(
        label=_("E-mail"),
        widget=forms.EmailInput(attrs={'placeholder': _('votre@email.com'), 'class': 'form-input'})
    )
    subject = forms.CharField(
        label=_("Sujet"),
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': _('Le sujet de votre message'), 'class': 'form-input'})
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={'placeholder': _('Comment pouvons-nous vous aider ?'), 'class': 'form-input', 'rows': 5})
    )
