from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from catalogue.models import Show, Review, Location, Locality

class PressCriticUseCaseTest(TestCase):
    """
    Test Case pour le Use Case : 
    Le critique de presse est un membre qui pourra soumettre à publication 
    un article critique à propos d'un spectacle.
    """
    @classmethod
    def setUpTestData(cls):
        # 1. Création du groupe PRESS_CRITIC
        cls.press_group, _ = Group.objects.get_or_create(name='PRESS_CRITIC')

        # 2. Attribution de la permission add_review au groupe PRESS_CRITIC
        try:
            permission = Permission.objects.get(codename='add_review', content_type__app_label='catalogue')
            cls.press_group.permissions.add(permission)
        except Permission.DoesNotExist:
            # Fallback si les permissions ne sont pas encore créées
            pass

        # 3. Création du membre Critique de Presse
        cls.press_user = User.objects.create_user(username='critique_pro', password='password123')
        cls.press_user.groups.add(cls.press_group)

        # 4. Création d'un spectacle pour le test
        cls.locality = Locality.objects.create(postal_code='1000', locality='Bruxelles')
        cls.location = Location.objects.create(
            slug='theatre-national',
            designation='Théâtre National',
            address='Boulevard Emile Jacqmain 111',
            locality=cls.locality
        )
        cls.show = Show.objects.create(
            slug='hamlet-2026',
            title='Hamlet',
            description='Une version moderne de Shakespeare',
            poster='hamlet.jpg',
            bookable=True,
            created_in=2026,
            location=cls.location
        )

    def test_press_critic_can_submit_review(self):
        """
        Vérifie qu'un membre du groupe PRESS_CRITIC peut soumettre une critique
        et qu'elle est stockée correctement (non publiée par défaut).
        """
        # Se connecter en tant que critique
        self.client.login(username='critique_pro', password='password123')
        
        # Données de la critique
        data = {
            'show': self.show.id,
            'review': 'Une mise en scène époustouflante qui redonne vie au texte de Shakespeare.',
            'stars': 5,
        }
        
        # Soumission de la critique
        response = self.client.post(reverse('catalogue:review-create'), data)
        
        # 302 car la vue redirige après succès
        self.assertEqual(response.status_code, 302)
        
        # Vérification en base de données
        review_count = Review.objects.filter(user=self.press_user, show=self.show).count()
        self.assertEqual(review_count, 1)
        
        review = Review.objects.get(user=self.press_user, show=self.show)
        self.assertEqual(review.review, data['review'])
        self.assertEqual(review.stars, 5)
        # Elle doit être non validée par défaut (pour soumission à publication)
        self.assertFalse(review.validated)

    def test_member_without_reservation_is_redirected(self):
        """
        Vérifie qu'un membre sans réservation est redirigé vers le détail du spectacle 
        avec un message d'erreur lorsqu'il tente de commenter.
        """
        normal_user = User.objects.create_user(username='simple_member', password='password123')
        # On doit lui donner le groupe MEMBER pour qu'il ait la permission add_review
        member_group = Group.objects.get(name='MEMBER')
        normal_user.groups.add(member_group)
        
        self.client.login(username='simple_member', password='password123')
        
        data = {
            'show': self.show.id,
            'review': 'Je tente ma chance sans billet.',
            'stars': 4,
        }
        
        # Tentative de soumission
        response = self.client.post(reverse('catalogue:review-create'), data)
        
        # Doit être redirigé vers le détail du spectacle (302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(reverse('frontend:show_detail', kwargs={'pk': self.show.id})))
        self.assertEqual(Review.objects.count(), 0)

    def test_member_with_reservation_can_submit_review(self):
        """
        Vérifie qu'un membre ayant une réservation confirmée peut poster son avis.
        """
        from catalogue.models import Reservation, Representation, RepresentationReservation, Price
        
        # 1. Préparation du membre
        member_user = User.objects.create_user(username='spectateur_fidele', password='password123')
        member_group = Group.objects.get(name='MEMBER')
        member_user.groups.add(member_group)
        self.client.login(username='spectateur_fidele', password='password123')
        
        # 2. Création de la réservation confirmée
        representation = Representation.objects.create(show=self.show, schedule='2026-05-01 20:00:00+02:00')
        price_obj = Price.objects.create(
            type='Standard', 
            price=20.0, 
            description='Place standard',
            start_date='2026-01-01',
            end_date='2026-12-31'
        )
        reservation = Reservation.objects.create(user=member_user, status='Confirmed')
        RepresentationReservation.objects.create(
            reservation=reservation, 
            representation=representation, 
            price=price_obj,
            quantity=2
        )
        
        # 3. Soumission de l'avis
        data = {
            'show': self.show.id,
            'review': 'J\'y étais, c\'était génial !',
            'stars': 5,
        }
        response = self.client.post(reverse('catalogue:review-create'), data)
        
        # Succès (redirection vers le spectacle)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.filter(user=member_user).count(), 1)

    from unittest.mock import patch

    @patch('requests.get')
    def test_validated_reviews_are_displayed_on_show_detail(self, mock_get):
        """
        Vérifie que seules les critiques validées sont affichées sur la page de détail.
        """
        # Créer une critique validée
        Review.objects.create(
            user=self.press_user,
            show=self.show,
            review='Critique validée',
            stars=5,
            validated=True
        )
        # Créer une critique non validée
        Review.objects.create(
            user=self.press_user,
            show=self.show,
            review='Critique non validée',
            stars=1,
            validated=False
        )

        # On simule la réponse de l'API avec les données de l'objet de test
        from api.serializers.shows import ShowSerializer
        serializer = ShowSerializer(self.show)
        mock_get.return_value.json.return_value = serializer.data
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status.return_value = None
        
        # Accéder à la page de détail (via le frontend qui utilise l'API)
        response = self.client.get(reverse('frontend:show_detail', kwargs={'pk': self.show.id}))
        
        self.assertEqual(response.status_code, 200)
        # Vérifier que le texte de la critique validée est présent
        self.assertContains(response, 'Critique validée')
        # Vérifier que le texte de la critique non validée n'est pas présent
        self.assertNotContains(response, 'Critique non validée')

    def test_admin_cannot_edit_other_user_review(self):
        """
        Vérifie que même un administrateur ne peut pas éditer le texte d'une critique
        dont il n'est pas l'auteur (Propriété Exclusive).
        """
        # Créer une critique par le critique de presse
        review = Review.objects.create(
            user=self.press_user,
            show=self.show,
            review='Texte original intouchable',
            stars=5,
            validated=True
        )
        
        # Créer et connecter un admin
        admin_user = User.objects.create_superuser(username='admin_boss', password='password123', email='admin@test.com')
        self.client.login(username='admin_boss', password='password123')
        
        # Tenter d'accéder à la page d'édition de la critique de press_user
        response = self.client.get(reverse('catalogue:review-edit', kwargs={'review_id': review.id}))
        
        # Doit rediriger avec un message d'erreur (302)
        self.assertEqual(response.status_code, 302)
        
        # Tenter de soumettre une modification
        data = {
            'show': self.show.id,
            'review': 'Texte modifié par admin',
            'stars': 1,
        }
        response = self.client.post(reverse('catalogue:review-edit', kwargs={'review_id': review.id}), data)
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que le texte n'a PAS changé en base
        review.refresh_from_db()
        self.assertEqual(review.review, 'Texte original intouchable')
