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

    def setUp(self):
        """
        Ce qui est exécuté avant chaque test.
        """
        self.client.force_authenticate(user=self.user)

    def test_list_prices(self):
        """
        Vérifie que la liste des prix peut être récupérée.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_price(self):
        """
        Vérifie qu'un prix peut être récupéré par son ID.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], self.price1.type)

    def test_create_price(self):
        """
        Vérifie qu'un nouveau prix peut être créé.
        """
        data = {
            "type": "Senior",
            "price": "20.00",
            "description": "Tarif pour les plus de 65 ans",
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Price.objects.count(), 3)
        self.assertEqual(response.data['type'], 'Senior')

    def test_update_price(self):
        """
        Vérifie qu'un prix peut être mis à jour.
        """
        data = {
            "type": "Adulte",
            "price": "28.50",
            "description": "Nouveau tarif normal",
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.price1.refresh_from_db()
        self.assertEqual(self.price1.price, 28.50)

    def test_delete_price(self):
        """
        Vérifie qu'un prix peut être supprimé.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Price.objects.count(), 1)
