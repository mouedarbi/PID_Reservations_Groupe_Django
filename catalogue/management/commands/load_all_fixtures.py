import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load all fixtures in the correct order.'

    def handle(self, *args, **options):
        # The order of fixtures to load
        fixture_files = [
            'auth_user.json',
            'localities.json',
            'types.json',
            'prices.json',
            'artists.json',
            'artist_type.json',
            'locations.json',
            'shows.json',
            'representations.json',
            'reviews.json',
            'user_meta.json',
            'reservations.json',
            'representation_reservations.json',
        ]

        # Rename ArtistFixtures.json to artists.json for clarity
        fixture_dir = os.path.join('catalogue', 'fixtures')
        old_artist_fixture_path = os.path.join(fixture_dir, 'ArtistFixtures.json')
        new_artist_fixture_path = os.path.join(fixture_dir, 'artists.json')

        if os.path.exists(old_artist_fixture_path):
            if not os.path.exists(new_artist_fixture_path):
                os.rename(old_artist_fixture_path, new_artist_fixture_path)
                self.stdout.write(self.style.SUCCESS('Successfully renamed "ArtistFixtures.json" to "artists.json"'))
            else:
                self.stdout.write(self.style.WARNING('"artists.json" already exists. Skipping rename.'))

        # Call loaddata for each fixture
        for fixture_file in fixture_files:
            self.stdout.write(self.style.SUCCESS(f'Loading fixture {fixture_file}...'))
            try:
                call_command('loaddata', fixture_file)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading fixture {fixture_file}: {e}'))
                # Decide if you want to stop on error or continue
                # For now, we stop.
                return

        self.stdout.write(self.style.SUCCESS('All fixtures loaded successfully.'))
