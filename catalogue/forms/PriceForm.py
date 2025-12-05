from django.forms import ModelForm
from catalogue.models import Price

class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = ['type', 'price', 'description', 'start_date', 'end_date']
