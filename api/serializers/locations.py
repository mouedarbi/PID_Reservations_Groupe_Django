from rest_framework import serializers
from catalogue.models import Location

class LocationSerializer(serializers.ModelSerializer):
    website = serializers.CharField(max_length=255, required=False, allow_null=True, default=None)
    
    class Meta:
        model = Location
        fields = '__all__'