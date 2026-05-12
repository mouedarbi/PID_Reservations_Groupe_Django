from rest_framework import serializers
from catalogue.models import Show, Review, PressArticle
from catalogue.models.show_price import ShowPrice
from api.serializers.representations import RepresentationSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'review', 'stars', 'validated', 'is_pinned', 'created_at']

class PressArticleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    show_title = serializers.CharField(source='show.title', read_only=True)
    show_poster = serializers.ImageField(source='show.poster', read_only=True)

    class Meta:
        model = PressArticle
        fields = ['id', 'user_name', 'show_title', 'show_poster', 'title', 'summary', 'content', 'validated', 'is_pinned', 'created_at']

class ShowSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    has_multiple_prices = serializers.ReadOnlyField()
    next_representation_date = serializers.ReadOnlyField()
    formatted_next_date = serializers.SerializerMethodField()
    poster = serializers.ImageField(use_url=True, required=False, allow_null=True)
    representations = RepresentationSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    press_articles = serializers.SerializerMethodField()
    
    # Nouveaux champs pour Genre et Artistes
    genre_name = serializers.CharField(source='genre.name_fr', read_only=True, default='')
    artists_list = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = '__all__'
        depth = 1

    def get_artists_list(self, obj):
        """Retourne la liste des noms complets des artistes participants."""
        # On passe par ArtistTypeShow -> ArtistType -> Artist
        artist_names = []
        for ats in obj.artistTypeShows.all().select_related('artist_type__artist'):
            artist = ats.artist_type.artist
            name = f"{artist.firstname} {artist.lastname}".strip()
            if name and name not in artist_names:
                artist_names.append(name)
        return artist_names

    def to_representation(self, instance):
        """
        Personnalise les données retournées selon le niveau d'affiliation.
        """
        data = super().to_representation(instance)
        request = self.context.get('request')

        # Par défaut, si pas de requête (ex: shell), on laisse tout
        if not request:
            return data

        # Si l'utilisateur est un affilié
        if hasattr(request, 'affiliate'):
            tier = request.affiliate.tier.name if request.affiliate.tier else 'Free'

            # CAS FREE : On garde l'ID et les infos de base pour l'affichage catalogue
            if tier == 'Free':
                allowed_fields = ['id', 'title', 'description', 'slug', 'formatted_next_date', 'price', 'poster']
                return {field: data[field] for field in allowed_fields if field in data}

            # CAS STARTER : On ajoute le poster et les artistes (depth=1 inclut les artistes par défaut)
            elif tier == 'Starter':
                # On retire les représentations, les reviews et articles de presse pour le plan Starter
                data.pop('representations', None)
                data.pop('reviews', None)
                data.pop('press_articles', None)
                data.pop('price', None)
                return data

        return data

    def get_formatted_next_date(self, obj):
        from django.utils import timezone
        from django.utils.formats import date_format
        next_rep = obj.representations.filter(schedule__gte=timezone.now()).order_by('schedule').first()
        if next_rep:
            return date_format(next_rep.schedule, "d M Y")
        return None

    def get_price(self, obj):
        # Retrieve all ShowPrice objects related to the current Show
        show_prices = obj.showprice_set.all()

        if show_prices.exists():
            # Get all actual price values from the related Price objects
            # Note: Each ShowPrice object has a 'price' ForeignKey to the Price model,
            # and the Price model itself has a 'price' DecimalField.
            prices = [sp.price.price for sp in show_prices]
            # Return the minimum price found
            return min(prices)
        return None # Or 0.0 if you prefer a default numeric value when no price is found

    def get_reviews(self, obj):
        # On ne retourne que les critiques validées pour le frontend
        validated_reviews = obj.reviews.filter(validated=True)
        return ReviewSerializer(validated_reviews, many=True).data

    def get_press_articles(self, obj):
        # On ne retourne que les articles validés par le producteur
        validated_articles = obj.press_articles.filter(validated=True)
        return PressArticleSerializer(validated_articles, many=True).data