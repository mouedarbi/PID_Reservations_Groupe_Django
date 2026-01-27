from rest_framework import serializers
from catalogue.models import Show

class ShowSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = '__all__'
        depth = 1

    def get_price(self, obj):
        # Temporary: returns a fixed price.
        # In a real scenario, this would compute the min price from representations.
        return 25.00 # Hardcoded price for now