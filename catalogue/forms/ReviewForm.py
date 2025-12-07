from django import forms
from catalogue.models.review import Review


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer / modifier un avis (Review).
    """

    class Meta:
        model = Review
        fields = "__all__"
