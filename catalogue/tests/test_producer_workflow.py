from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from catalogue.models import ProducerRequest, Show, Location
from django.core.files.uploadedfile import SimpleUploadedFile

class ProducerWorkflowTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create groups
        self.member_group, _ = Group.objects.get_or_create(name='MEMBER')
        self.producer_group, _ = Group.objects.get_or_create(name='PRODUCER')
        
        # Create a member user
        self.user = User.objects.create_user(username='member_user', password='password123', email='member@test.com')
        self.user.groups.add(self.member_group)
        
        # Create an admin user
        self.admin = User.objects.create_superuser(username='admin_user', password='password123', email='admin@test.com')
        
        # Create a locality
        from catalogue.models import Locality
        self.locality = Locality.objects.create(postal_code='1000', locality='Brussels')
        
        # Create a location for shows
        self.location = Location.objects.create(
            slug='test-location', 
            designation='Test Location', 
            address='123 Test St',
            locality=self.locality
        )

    def test_full_producer_workflow(self):
        # 1. Login as member
        self.client.login(username='member_user', password='password123')
        
        # 2. Submit producer request
        response = self.client.post(reverse('accounts:become_producer'), {
            'first_name': 'Mohamed',
            'last_name': 'Test',
            'address': '123 Producer Way',
            'email': 'mohamed@test.com',
            'phone': '0123456789',
            'presentation': 'I am a great producer.',
            'motivation': 'I want to share my shows.'
        })
        # Check if redirected or successful
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(ProducerRequest.objects.filter(user=self.user, status='pending').exists())
        
        # 3. Admin approves the request
        self.client.login(username='admin_user', password='password123')
        request_obj = ProducerRequest.objects.get(user=self.user)
        
        response = self.client.get(reverse('admin_producer_request_action', kwargs={'pk': request_obj.pk, 'action': 'approve'}), follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify status and groups
        request_obj.refresh_from_db()
        self.assertEqual(request_obj.status, 'approved')
        self.user.refresh_from_db()
        self.assertIn(self.producer_group, self.user.groups.all())
        self.assertNotIn(self.member_group, self.user.groups.all())
        
        # 4. Check profile display
        self.client.login(username='member_user', password='password123')
        response = self.client.get(reverse('accounts:user-profile'))
        self.assertEqual(response.status_code, 200)
        
        # Check for "Espace Producteur" in sidebar
        self.assertContains(response, "Espace Producteur")
        # Check if "Devenir Producteur?" is NOT present
        self.assertNotContains(response, "Devenir Producteur?")

    def test_producer_submits_show(self):
        # Setup: User is already a producer
        self.user.groups.clear()
        self.user.groups.add(self.producer_group)
        self.client.login(username='member_user', password='password123')
        
        # Ensure location has capacity
        self.location.capacity = 100
        self.location.save()
        
        # Submit a show with all required fields
        response = self.client.post(reverse('catalogue:prod_submit_show'), {
            'title': 'My New Show',
            'description': 'A great show description.',
            'duration': 90,
            'date': '2026-05-10',
            'time': '20:00',
            'location': self.location.id,
            'ticket_count': 50
        })
        
        # Check if redirected to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('catalogue:prod_dashboard'))
        
        # Verify database
        show = Show.objects.filter(title='My New Show').first()
        self.assertIsNotNone(show)
        self.assertEqual(show.producer, self.user)
        self.assertEqual(show.status, 'pending')
        
        # Check if representation was created
        from catalogue.models import Representation
        rep = Representation.objects.filter(show=show).first()
        self.assertIsNotNone(rep)
        self.assertEqual(rep.total_seats, 50)
        self.assertEqual(rep.available_seats, 50)
