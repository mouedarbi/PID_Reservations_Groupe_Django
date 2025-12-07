from rest_framework.response import Response
from rest_framework.views import APIView

class LocationsView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)

class LocationsDetailView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)