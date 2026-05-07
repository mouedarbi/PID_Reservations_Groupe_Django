from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from catalogue.models import CriticRequest, PressArticle, Show, Location, Locality

class PressSystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create groups
        self.member_group, _ = Group.objects.get_or_create(name='MEMBER')
        self.producer_group, _ = Group.objects.get_or_create(name='PRODUCER')
        self.critic_group, _ = Group.objects.get_or_create(name='PRESS_CRITIC')
        
        # Create users
        self.member = User.objects.create_user(username='member', password='password123')
        self.member.groups.add(self.member_group)
        
        self.producer = User.objects.create_user(username='producer', password='password123')
        self.producer.groups.add(self.producer_group)
        
        self.admin = User.objects.create_superuser(username='admin', password='password123')
        
        # Setup show
        self.locality = Locality.objects.create(postal_code='1000', locality='Brussels')
        self.location = Location.objects.create(slug='loc', designation='Loc', address='Add', locality=self.locality, capacity=100)
        self.show = Show.objects.create(slug='show', title='Show', location=self.location, producer=self.producer, status='published', created_in=2026)

    def test_critic_workflow(self):
        # 1. Member requests to become critic
        self.client.login(username='member', password='password123')
        response = self.client.post(reverse('accounts:become_critic'), {
            'first_name': 'Jean',
            'last_name': 'Critique',
            'profession': 'Journaliste',
            'media_name': 'Le Soir',
            'motivation': 'J\'aime le théâtre.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CriticRequest.objects.filter(user=self.member, status='pending').exists())
        
        # 2. Admin approves
        self.client.login(username='admin', password='password123')
        req = CriticRequest.objects.get(user=self.member)
        response = self.client.post(reverse('admin_critic_request_action', kwargs={'pk': req.pk, 'action': 'approve'}))
        self.assertEqual(response.status_code, 302)
        
        self.member.refresh_from_db()
        self.assertIn(self.critic_group, self.member.groups.all())
        
        # 3. Critic submits article
        self.client.login(username='member', password='password123')
        response = self.client.post(reverse('catalogue:submit_press_article'), {
            'show': self.show.id,
            'title': 'Superbe spectacle',
            'summary': 'Un résumé court.',
            'content': 'Un contenu très long et détaillé.'
        })
        self.assertEqual(response.status_code, 302)
        article = PressArticle.objects.get(title='Superbe spectacle')
        self.assertFalse(article.validated)
        
        # 4. Producer moderates
        self.client.login(username='producer', password='password123')
        # Check if visible in moderate list
        response = self.client.get(reverse('catalogue:prod_moderate_press_articles'))
        self.assertContains(response, 'Superbe spectacle')
        
        # Approve it
        response = self.client.get(reverse('catalogue:prod_validate_press_article', kwargs={'pk': article.pk, 'action': 'approve'}))
        article.refresh_from_db()
        self.assertTrue(article.validated)
        
        # 5. Check database state
        article.refresh_from_db()
        self.assertTrue(article.validated)
        self.assertEqual(article.show.press_articles.filter(validated=True).count(), 1)
