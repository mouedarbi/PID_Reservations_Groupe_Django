from django import forms
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {
            'name': 'Nom du groupe',
            'permissions': 'Droits d\'accès / Permissions',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ex: Administrateurs, Clients, etc.'}),
            'permissions': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'permissions': 'Sélectionnez les actions autorisées pour ce groupe.',
        }
