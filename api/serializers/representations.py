from rest_framework import serializers
from catalogue.models import Representation
from django.utils.translation import gettext as _
from django.utils.formats import date_format

class RepresentationSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Representation
        fields = ['id', 'show', 'schedule', 'formatted_date', 'location', 'available_seats']

    def get_formatted_date(self, obj):
        if not obj.schedule:
            return None
        # Format localized date and time
        d = date_format(obj.schedule, "d F Y")
        t = date_format(obj.schedule, "H:i")
        return f"{d} {_('à')} {t}"