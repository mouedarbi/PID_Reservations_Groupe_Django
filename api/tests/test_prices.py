# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalogue.models import Price
from django.contrib.auth import get_user_model

User = get_user_model()

class PriceAPITests(APITestCase):
    """
    Tests pour l'API Price.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Mise en place des données initiales pour tous les tests de cette classe.
        """
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.admin_user = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com')
        
        cls.price1 = Price.objects.create(
            type="Adulte",
            price=25.00,
            description="Tarif normal",
            start_date="2026-01-01",
            end_date="2026-12-31"
        )
        cls.price2 = Price.objects.create(
            type="Enfant",
            price=15.00,
            description="Tarif réduit pour les moins de 12 ans",
            start_date="2026-01-01",
            end_date="2026-12-31"
        )
        
        cls.list_url = reverse('api:prices-list-create')
        cls.detail_url = reverse('api:prices-detail', kwargs={'id': cls.price1.id})
        cls.invalid_detail_url = reverse('api:prices-detail', kwargs={'id': 9999}) # Pour tester les IDs inexistants

    def test_list_prices_unauthenticated(self):
        """
        Vérifie que les utilisateurs non authentifiés peuvent lister les prix (lecture seule).
        """
        self.client.force_authenticate(user=None) # S'assurer que le client n'est pas authentifié
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_prices_authenticated(self):
        """
        Vérifie que les utilisateurs authentifiés peuvent lister les prix.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_price_unauthenticated(self):
        """
        Vérifie que les utilisateurs non authentifiés ne peuvent pas créer de prix.
        """
        data = {
            "type": "Senior", "price": "20.00", "description": "Tarif Senior",
            "start_date": "2026-01-01", "end_date": "2026-12-31"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Price.objects.count(), 2)

    def test_create_price_authenticated_non_admin(self):
        """
        Vérifie que les utilisateurs authentifiés non-admin peuvent créer des prix.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "type": "Senior", "price": "20.00", "description": "Tarif Senior",
            "start_date": "2026-01-01", "end_date": "2026-12-31"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Price.objects.count(), 3)

    def test_retrieve_price_unauthenticated(self):
        """
        Vérifie que les utilisateurs non authentifiés ne peuvent pas récupérer un prix spécifique.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_price_authenticated_non_admin(self):
        """
        Vérifie que les utilisateurs authentifiés non-admin ne peuvent pas récupérer un prix spécifique.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_price_admin(self):
        """
        Vérifie que les administrateurs peuvent récupérer un prix spécifique.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], self.price1.type)

    def test_update_price_unauthenticated(self):
        """
        Vérifie que les utilisateurs non authentifiés ne peuvent pas mettre à jour un prix.
        """
        self.client.force_authenticate(user=None)
        data = {"type": "Modifié", "price": "30.00", "description": "Modifié", "start_date": "2026-01-01", "end_date": "2026-12-31"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_price_authenticated_non_admin(self):
        """
        Vérifie que les utilisateurs authentifiés non-admin ne peuvent pas mettre à jour un prix.
        """
        self.client.force_authenticate(user=self.user)
        data = {"type": "Modifié", "price": "30.00", "description": "Modifié", "start_date": "2026-01-01", "end_date": "2026-12-31"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_price_admin(self):
        """
        Vérifie que les administrateurs peuvent mettre à jour un prix.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {"type": "Modifié", "price": "30.00", "description": "Modifié", "start_date": "2026-01-01", "end_date": "2026-12-31"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.price1.refresh_from_db()
        self.assertEqual(self.price1.price, 30.00)

    def test_delete_price_unauthenticated(self):
        """
        Vérifie que les utilisateurs non authentifiés ne peuvent pas supprimer un prix.
        """
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Price.objects.count(), 2)

    def test_delete_price_authenticated_non_admin(self):
        """
        Vérifie que les utilisateurs authentifiés non-admin ne peuvent pas supprimer un prix.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Price.objects.count(), 2)

    def test_delete_price_admin(self):
        """
        Vérifie que les administrateurs peuvent supprimer un prix.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Price.objects.count(), 1)