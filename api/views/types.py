from rest_framework.response import Response
from rest_framework.views import APIView
from catalogue.models import Type
from api.serializers.types import TypeSerializer

class TypesView(APIView):
    def get(self, request, *args, **kwargs):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)

class TypesDetailView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            type = Type.objects.get(pk=pk)
        except Type.DoesNotExist:
            return Response({"error": "Type not found"}, status=404)

        serializer = TypeSerializer(type)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        try:
            type = Type.objects.get(pk=pk)
        except Type.DoesNotExist:
            return Response({"error": "Type not found"}, status=404)
        serializer = TypeSerializer(artist)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)