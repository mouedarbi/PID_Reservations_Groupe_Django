from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny # Added import
from catalogue.models import Show
from api.serializers.shows import ShowSerializer

class ShowsView(APIView):
    """
    API view to get a list of all shows.
    """
    authentication_classes = [] # Temporarily disable authentication
    permission_classes = [AllowAny] # Temporarily allow any user

    def get(self, request, *args, **kwargs):
        """
        Return a list of all shows.
        """
        shows = Show.objects.all()
        # Passing context is good practice for serializers that use it (e.g., for hyperlinks)
        serializer = ShowSerializer(shows, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder for creating shows"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder for updating shows"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder for deleting shows"}, status=501)

class ShowsDetailView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)

class ShowsSearchView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)