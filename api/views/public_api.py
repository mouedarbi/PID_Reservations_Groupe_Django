from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from catalogue.models import Show, Representation
from api.serializers.shows import ShowSerializer
from api.serializers.representations import RepresentationSerializer

class PublicShowsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Retourne la liste publique des spectacles (infos de base uniquement).
        On simule un affilié 'Free' pour forcer le filtrage des champs.
        """
        shows = Show.objects.all()
        # On passe un contexte factice pour forcer le comportement 'Free' si nécessaire
        # ou on laisse le serializer gérer l'absence d'affilié dans la requête.
        serializer = ShowSerializer(shows, many=True, context={'request': request})
        
        # Filtrage manuel supplémentaire si le serializer n'est pas assez restrictif par défaut
        data = serializer.data
        allowed_fields = ['id', 'title', 'description', 'slug', 'poster']
        filtered_data = []
        for show in data:
            filtered_data.append({k: v for k, v in show.items() if k in allowed_fields})
            
        return Response(filtered_data)

class PublicRepresentationsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Retourne la liste publique des représentations.
        """
        representations = Representation.objects.all()
        serializer = RepresentationSerializer(representations, many=True)
        return Response(serializer.data)