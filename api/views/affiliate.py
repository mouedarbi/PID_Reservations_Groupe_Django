from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.authentication import ApiKeyAuthentication
from catalogue.models import Show, Representation
from api.serializers.shows import ShowSerializer
from api.serializers.representations import RepresentationSerializer

class AffiliateShowsView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retourne la liste des spectacles. Les champs retournés dépendent du plan (tier) de l'affilié.
        La logique de filtrage par tier est déjà dans ShowSerializer.to_representation.
        """
        shows = Show.objects.all()
        serializer = ShowSerializer(shows, many=True, context={'request': request})
        return Response(serializer.data)

class AffiliateRepresentationsView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retourne la liste des représentations.
        """
        representations = Representation.objects.all()
        serializer = RepresentationSerializer(representations, many=True)
        return Response(serializer.data)

class AffiliateSubscriptionView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retourne les informations sur l'abonnement actuel de l'affilié.
        """
        affiliate = request.affiliate
        return Response({
            "tier": affiliate.tier.name if affiliate.tier else "None",
            "api_limit_daily": affiliate.tier.api_limit_daily if affiliate.tier else 0,
            "price": str(affiliate.tier.price) if affiliate.tier else "0.00",
            "is_active": affiliate.is_active
        })