import os
import django
from django.utils import translation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Show
from api.serializers.shows import ShowSerializer

def test_serializer():
    show = Show.objects.get(pk=2) # Cible mouvante / Moving Target
    print(f"Testing Show ID: {show.id}")
    
    for lang in ['fr', 'en', 'nl']:
        with translation.override(lang):
            serializer = ShowSerializer(show)
            data = serializer.data
            print(f"[{lang}] Serialized title: {data.get('title')}")

if __name__ == "__main__":
    test_serializer()
