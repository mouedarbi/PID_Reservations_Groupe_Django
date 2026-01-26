from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone

from catalogue.models import Representation
from api.serializers.representations import RepresentationSerializer

# For a true RSS feed, you would typically use a custom renderer.
# You could add this to your settings.py:
# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#         'api.renderers.RSSRenderer',  # Your custom renderer
#     ]
# }
# For now, this view will return JSON data suitable for a feed.

class RssNextRepresentationsView(APIView):
    """
    Provides data for the next 50 upcoming representations.
    """
    def get(self, request, *args, **kwargs):
        now = timezone.now()
        
        # Get the 50 next upcoming representations
        upcoming_representations = Representation.objects.filter(
            when__gte=now
        ).order_by('when')[:50]

        serializer = RepresentationSerializer(upcoming_representations, many=True)

        # The data is structured here. A custom renderer would take this
        # data and format it into an RSS XML structure.
        feed_data = {
            "title": "Prochaines représentations",
            "description": "Liste des 50 prochaines représentations à venir.",
            "link": request.build_absolute_uri(),
            "items": serializer.data,
        }

        return Response(feed_data, status=status.HTTP_200_OK)