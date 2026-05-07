from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from catalogue.models import PressArticle
from api.serializers.shows import PressArticleSerializer

class PublicPressArticlePagination(PageNumberPagination):
    page_size = 4

class PressArticleListView(APIView):
    """
    API view to list validated press articles for the public blog.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        articles = PressArticle.objects.filter(validated=True).select_related('user', 'show').order_by('-is_pinned', '-created_at')
        
        paginator = PublicPressArticlePagination()
        page = paginator.paginate_queryset(articles, request)
        
        if page is not None:
            # We want to include show info (title, poster) in the article serializer for the blog
            # I might need a slightly richer serializer for the list
            serializer = PressArticleSerializer(page, many=True)
            # Add show data manually if needed or update serializer
            # The current PressArticleSerializer in api/serializers/shows.py only has show name/id? 
            # Let's check it.
            return paginator.get_paginated_response(serializer.data)
            
        serializer = PressArticleSerializer(articles, many=True)
        return Response(serializer.data)

class PressArticleDetailView(APIView):
    """
    API view to get a single press article.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk, *args, **kwargs):
        article = PressArticle.objects.get(pk=pk, validated=True)
        serializer = PressArticleSerializer(article)
        return Response(serializer.data)
