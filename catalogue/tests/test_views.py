from django.test import TestCase
from django.urls import reverse
from catalogue.models import Show, Location, Locality

class ShowViewsTest(TestCase):
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

    def test_show_index_view(self):
        response = self.client.get(reverse('catalogue:show-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show/index.html')
        self.assertContains(response, "Hamlet")

    def test_show_detail_view(self):
        response = self.client.get(reverse('catalogue:show-show', args=[self.show.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show/show.html')
        self.assertContains(response, "Hamlet")
        self.assertContains(response, "La célèbre pièce de Shakespeare")

    def test_show_detail_view_404(self):
        # Tester un spectacle qui n'existe pas
        response = self.client.get(reverse('catalogue:show-show', args=[999]))
        self.assertEqual(response.status_code, 404)
