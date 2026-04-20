from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from catalogue.models import Locality, Location, Type, Artist, Show, Price, Representation, ShowPrice, Review
from django.utils import timezone
import datetime

class AdminUseCasesTest(TestCase):
    """
    Série de tests basés sur les Cas d'Utilisation (Use Cases) de l'administration.
    L'ordre des fixtures respecte la logique métier du projet.
    """
    fixtures = [
        'auth_user.json',
        'localities.json',
        'types.json',
        'prices.json',
        'artists.json',
        'artist_type.json',
        'locations.json',
        'shows.json',
        'show_prices.json',
        'representations.json'
    ]

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='test_admin_boss',
            email='admin@boss.com',
            password='password123'
        )
        self.client.login(username='test_admin_boss', password='password123')

    def test_use_case_1_technical_setup(self):
        """
        USE CASE 1 : Configuration Technique du Référentiel.
        """
        print("\n--- Running Use Case 1: Technical Setup ---")

        # 1. Ajout d'une nouvelle localité
        print("Step 1: Adding a new Locality...")
        response = self.client.post(reverse('admin_locality_create'), {
            'postal_code': '1410',
            'locality_fr': 'Waterloo',
            'locality_en': 'Waterloo',
            'locality_nl': 'Waterloo'
        })
        if response.status_code != 302:
            print(f"Error creating locality: {response.status_code}")
            if hasattr(response, 'context') and response.context and 'form' in response.context:
                print(f"Form errors: {response.context['form'].errors}")
        self.assertTrue(Locality.objects.filter(locality_fr='Waterloo').exists())
        waterloo = Locality.objects.get(locality='Waterloo')

        # 2. Création d'un lieu (Correction: ajout de phone)
        print("Step 2: Creating a Location...")
        response = self.client.post(reverse('admin_location_create'), {
            'slug': 'nouveau-theatre',
            'designation': 'Nouveau Théâtre',
            'address': 'Rue du Test 1',
            'locality': waterloo.id,
            'website': 'https://test.be',
            'phone': '023456789'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Location.objects.filter(slug='nouveau-theatre').exists())

        print("Use Case 1 completed successfully!")

    def test_use_case_2_show_publishing(self):
        """
        USE CASE 2 : Mise en ligne d'un Spectacle.
        """
        print("\n--- Running Use Case 2: Show Publishing ---")

        # 1. Création Artiste
        print("Step 1: Creating a new Artist...")
        response = self.client.post(reverse('admin_artist_create'), {'firstname': 'Moliere', 'lastname': 'Le Jeune'})
        self.assertEqual(response.status_code, 302)
        jean = Artist.objects.get(lastname='Le Jeune')

        # 2. Création Spectacle (Correction: ajout de poster_url)
        print("Step 2: Creating a new Show...")
        location = Location.objects.first()
        response = self.client.post(reverse('admin_show_create'), {
            'slug': 'l-avare-2024',
            'title': 'L\'Avare 2024',
            'description': 'Classique revisité.',
            'poster': 'https://test.be/poster.jpg',
            'duration': 90,
            'created_in': 2024,
            'location': location.id,
            'bookable': True
        })
        self.assertEqual(response.status_code, 302)
        show = Show.objects.get(slug='l-avare-2024')

        # 3. Ajout Prix
        print("Step 3: Associating a Price...")
        price = Price.objects.get(type='adult')
        response = self.client.post(reverse('admin_show_detail', args=[show.id]), {'price_id': price.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ShowPrice.objects.filter(show=show, price=price).exists())

        print("Use Case 2 completed successfully!")

    def test_use_case_3_community_management(self):
        """
        USE CASE 3 : Gestion de la Communauté.
        """
        print("\n--- Running Use Case 3: Community Management ---")

        # 1. Groupe
        print("Step 1: Creating a Group 'Managers'...")
        perm = Permission.objects.get(codename='change_show')
        response = self.client.post(reverse('admin_group_create'), {
            'name': 'Managers',
            'permissions': [perm.id]
        })
        self.assertEqual(response.status_code, 302)
        managers_group = Group.objects.get(name='Managers')

        # 2. Utilisateur
        print("Step 2: Assigning Group to a User...")
        user = User.objects.create_user(username='staff_member', password='password123')
        response = self.client.post(reverse('admin_user_edit', args=[user.id]), {
            'username': 'staff_member',
            'first_name': 'Staff',
            'last_name': 'Member',
            'email': 'staff@theatre.be',
            'is_active': True,
            'is_staff': True,
            'groups': [managers_group.id],
            'langue': 'fr'
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertIn(managers_group, user.groups.all())

        print("Use Case 3 completed successfully!")
