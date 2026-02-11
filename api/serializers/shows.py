from rest_framework import serializers
from catalogue.models import Show
from catalogue.models.show_price import ShowPrice

class ShowSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = '__all__'
        depth = 1

    def get_price(self, obj):
        # Retrieve all ShowPrice objects related to the current Show
        show_prices = obj.showprice_set.all()

        if show_prices.exists():
            # Get all actual price values from the related Price objects
            # Note: Each ShowPrice object has a 'price' ForeignKey to the Price model,
            # and the Price model itself has a 'price' DecimalField.
            prices = [sp.price.price for sp in show_prices]
            # Return the minimum price found
            return min(prices)
        return None # Or 0.0 if you prefer a default numeric value when no price is found