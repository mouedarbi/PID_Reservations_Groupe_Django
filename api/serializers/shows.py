from rest_framework import serializers
from catalogue.models import Show, Review
from catalogue.models.show_price import ShowPrice
from api.serializers.representations import RepresentationSerializer
from api.serializers.prices import PriceSerializer
from api.serializers.artist_types import ArtistTypeSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'review', 'stars', 'validated', 'created_at']

class ShowSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    prices = PriceSerializer(many=True, read_only=True)
    artist_types = ArtistTypeSerializer(many=True, read_only=True)
    representations = RepresentationSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

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

    def get_reviews(self, obj):
        # On ne retourne que les critiques validées pour le frontend
        validated_reviews = obj.reviews.filter(validated=True)
        return ReviewSerializer(validated_reviews, many=True).data