from rest_framework import serializers
from catalogue.models import Show

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'