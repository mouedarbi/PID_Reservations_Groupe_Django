from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Placeholder pour les vues qui ne sont pas encore implémentées
class PlaceholderView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def post(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)

def index(request):
    """
    Basic API index view
    """
    return JsonResponse({
        'message': 'Welcome to the Reservation API',
        'status': 'active'
    })