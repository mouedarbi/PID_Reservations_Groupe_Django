import os
import django
from django.utils import translation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Location, Show, Price, Locality

def check_translations():
    print("Checking Locality translations...")
    localities = Locality.objects.all()
    for loc in localities:
        print(f"ID: {loc.id}, Code: {loc.postal_code}")
        for lang in ['fr', 'en', 'nl']:
            with translation.override(lang):
                print(f"  [{lang}] locality: {loc.locality}")

    print("\nChecking Location translations...")
    locations = Location.objects.all()
    for loc in locations:
        print(f"ID: {loc.id}, Slug: {loc.slug}")
        for lang in ['fr', 'en', 'nl']:
            with translation.override(lang):
                print(f"  [{lang}] designation: {loc.designation}, address: {loc.address}")
    
    print("\nChecking Show translations...")
    shows = Show.objects.all()
    for show in shows:
        print(f"ID: {show.id}, Title: {show.title}")
        for lang in ['fr', 'en', 'nl']:
            with translation.override(lang):
                print(f"  [{lang}] title: {show.title}")

    print("\nChecking Price translations...")
    prices = Price.objects.all()
    for price in prices:
        print(f"ID: {price.id}, Type: {price.type}")
        for lang in ['fr', 'en', 'nl']:
            with translation.override(lang):
                print(f"  [{lang}] type: {price.type}")

if __name__ == "__main__":
    check_translations()
