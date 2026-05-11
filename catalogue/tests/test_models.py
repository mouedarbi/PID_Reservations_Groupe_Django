from django.test import TestCase
from catalogue.models import Locality, Location, Show, Price, ShowPrice
from django.core.exceptions import ValidationError
from datetime import date

class LocalityModelTest(TestCase):
    def test_locality_creation(self):
        locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")
        self.assertEqual(str(locality), "1000 Bruxelles")

class LocationModelTest(TestCase):
    def setUp(self):
        self.locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")

    def test_location_creation(self):
        location = Location.objects.create(
            slug="theatre-royal",
            designation="Théâtre Royal",
            address="Rue de la Régence 3",
            locality=self.locality,
            capacity=500
        )
        self.assertEqual(str(location), "Théâtre Royal")
        self.assertEqual(location.locality.locality, "Bruxelles")

class ShowModelTest(TestCase):
    def setUp(self):
        self.locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")
        self.location = Location.objects.create(
            slug="theatre-national",
            designation="Théâtre National",
            address="Boulevard Emile Jacqmain 111",
            locality=self.locality
        )
        self.show = Show.objects.create(
            slug="hamlet",
            title="Hamlet",
            description="La célèbre pièce de Shakespeare",
            created_in=2024,
            location=self.location,
            status='published'
        )
        self.price1 = Price.objects.create(
            type="Adulte",
            price=25.00,
            description="Tarif plein",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )
        self.price2 = Price.objects.create(
            type="Enfant",
            price=15.00,
            description="Moins de 12 ans",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )

    def test_show_creation(self):
        self.assertEqual(str(self.show), "Hamlet")
        self.assertEqual(self.show.status, 'published')

    def test_show_price_property(self):
        # Initialement, pas de prix
        self.assertIsNone(self.show.price)
        self.assertFalse(self.show.has_multiple_prices)

        # Ajouter un prix
        ShowPrice.objects.create(show=self.show, price=self.price1)
        self.assertEqual(self.show.price, 25.00)

        # Ajouter un deuxième prix (moins cher)
        ShowPrice.objects.create(show=self.show, price=self.price2)
        self.assertEqual(self.show.price, 15.00)
        self.assertTrue(self.show.has_multiple_prices)
