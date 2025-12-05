from django.forms import ModelForm
from catalogue.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['show', 'review', 'stars']
