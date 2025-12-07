
from django import forms
from catalogue.models.locality import Locality


class LocalityForm(forms.ModelForm):
    """
    Formulaire pour créer / modifier une Locality.
    """

    class Meta:
        model = Locality
        fields = "__all__"
