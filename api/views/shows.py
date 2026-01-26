from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from catalogue.models import Show
from api.serializers.shows import ShowSerializer

class ShowsView(APIView):
    """
    API view for listing and creating shows.
    """
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kwargs):
        """
        Return a list of all shows.
        """
        shows = Show.objects.all()
        serializer = ShowSerializer(shows, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder for creating shows"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder for updating shows"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder for deleting shows"}, status=501)

class ShowsDetailView(APIView):
    """
    API view to retrieve, update or delete a show instance.
    """
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, pk, *args, **kwargs):
        """
        Return details for a single show identified by primary key (pk).
        """
        try:
            show = Show.objects.get(pk=pk)
        except Show.DoesNotExist:
            return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShowSerializer(show, context={'request': request})
        return Response(serializer.data)
    
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
