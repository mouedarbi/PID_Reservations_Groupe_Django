from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from rest_framework import status
from catalogue.models import Show
from api.serializers.shows import ShowSerializer
from api.authentication import ApiKeyAuthentication

from rest_framework.pagination import PageNumberPagination

class ShowsView(APIView):
    """
    API view for listing and creating shows with Affiliate Plan support.
    """
    authentication_classes = [authentication.SessionAuthentication, ApiKeyAuthentication]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kwargs):
        """
        Return a list of shows. 
        - Public access: All published shows.
        - Affiliate access: Limited number of published shows based on tier.
        - Admin access: All shows.
        """
        if request.user.is_staff:
            shows_queryset = Show.objects.all().order_by('id')
        else:
            shows_queryset = Show.objects.filter(status='published').order_by('id')

        # 1. CAS : UTILISATEUR API (via X-Api-Key)
        if hasattr(request, 'affiliate'):
            tier = request.affiliate.tier.name if request.affiliate.tier else 'Free'
            
            if tier == 'Free':
                shows_queryset = shows_queryset[:2]  # Limite à 2 spectacles
            elif tier == 'Starter':
                shows_queryset = shows_queryset[:10] # Limite à 10 spectacles
            # Premium : pas de limite
            
        # 2. CAS : ACCÈS PUBLIC SANS CLÉ (ex: via navigateur ou appel interne frontend)
        # On ne bride pas l'accès public pour le site lui-même
        # Mais on s'assure que seuls les spectacles publiés sont vus (fait plus haut)

        # Pagination
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(shows_queryset, request)
        if page is not None:
            serializer = ShowSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = ShowSerializer(shows_queryset, many=True, context={'request': request})
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
