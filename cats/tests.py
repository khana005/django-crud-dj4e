from django.test import TestCase, Client
from django.contrib.auth.models import User
from cats.models import Breed, Cat

class CatsCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.breed = Breed.objects.create(name='Persian')

    def test_unauthenticated_redirect(self):
        client = Client()
        response = client.get('/cats/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_cat_list_and_meta_tags(self):
        client = Client()
        client.login(username='testuser', password='password123')
        response = client.get('/cats/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<meta name="dj4e" content="53a9b4c9e6f79b30153c60fc0463863b">', content)
        self.assertNotIn('dj4e-code', content)
        self.assertNotIn('42-42', content)

    def test_cat_crud_lifecycle(self):
        client = Client()
        client.login(username='testuser', password='password123')

        # Create Cat
        create_resp = client.post('/cats/main/create/', {
            'nickname': 'Whiskers',
            'weight': 10,
            'foods': 'Tuna',
            'breed': self.breed.id
        })
        self.assertEqual(create_resp.status_code, 302)
        cat = Cat.objects.get(nickname='Whiskers')
        self.assertEqual(cat.weight, 10)

        # Update Cat
        update_resp = client.post(f'/cats/main/{cat.id}/update/', {
            'nickname': 'Whiskers Deluxe',
            'weight': 12,
            'foods': 'Salmon',
            'breed': self.breed.id
        })
        self.assertEqual(update_resp.status_code, 302)
        cat.refresh_from_db()
        self.assertEqual(cat.nickname, 'Whiskers Deluxe')

        # Delete Cat
        delete_resp = client.post(f'/cats/main/{cat.id}/delete/')
        self.assertEqual(delete_resp.status_code, 302)
        self.assertFalse(Cat.objects.filter(id=cat.id).exists())

    def test_existing_endpoints_unbroken(self):
        client = Client()
        polls_resp = client.get('/polls/owner')
        self.assertEqual(polls_resp.status_code, 200)
        self.assertIn('53a9b4c9', polls_resp.content.decode('utf-8'))

        hello_resp = client.get('/hello/')
        self.assertEqual(hello_resp.status_code, 200)
        self.assertIn('view count=1', hello_resp.content.decode('utf-8'))
