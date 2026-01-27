from rest_framework import serializers
from catalogue.models.artist_type import ArtistType


class ArtistTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistType
        fields = "__all__"