from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAdminUser

from catalogue.models import Representation
from ..serializers.representations import RepresentationSerializer

class RepresentationsView(APIView):
    """
    LIST (GET): Public
    CREATE (POST): Admin only
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        show_id = request.query_params.get('show_id')
        location_id = request.query_params.get('location_id')
        
        representations = Representation.objects.all()
        
        if show_id:
            representations = representations.filter(show_id=show_id)
        if location_id:
            representations = representations.filter(location_id=location_id)
            
        serializer = RepresentationSerializer(representations, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = RepresentationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RepresentationsDetailView(APIView):
    """
    RETRIEVE (GET): Public
    UPDATE/DELETE: Admin only
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_object(self, pk):
        try:
            return Representation.objects.get(pk=pk)
        except Representation.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        representation = self.get_object(pk)
        serializer = RepresentationSerializer(representation)
        return Response(serializer.data)
    
    def put(self, request, pk, *args, **kwargs):
        representation = self.get_object(pk)
        serializer = RepresentationSerializer(representation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        representation = self.get_object(pk)
        serializer = RepresentationSerializer(representation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        representation = self.get_object(pk)
        representation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RepresentationsCalendarView(APIView):
    """
    GET: List representations by date range.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        
        representations = Representation.objects.all()
        
        if start_date:
            representations = representations.filter(schedule__gte=start_date)
        if end_date:
            representations = representations.filter(schedule__lte=end_date)
            
        serializer = RepresentationSerializer(representations, many=True)
        return Response(serializer.data)

class RepresentationsAvailabilityView(APIView):
    """
    GET: Return available seats for a representation.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        try:
            representation = Representation.objects.get(pk=pk)
            return Response({
                "representation_id": representation.id,
                "available_seats": representation.available_seats
            })
        except Representation.DoesNotExist:
            return Response({"error": "Representation not found"}, status=status.HTTP_404_NOT_FOUND)