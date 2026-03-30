from rest_framework import serializers
from catalogue.models import Representation

class RepresentationSerializer(serializers.ModelSerializer):
    formatted_date = serializers.DateTimeField(format="%d %B %Y à %H:%M", source='schedule', read_only=True)
    
    class Meta:
        model = Representation
        fields = ['id', 'show', 'schedule', 'formatted_date', 'location', 'available_seats']
        