from django.test import TestCase, Client

class MainViewTests(TestCase):
    def test_base_site(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('53a9b4c9', response.content.decode('utf-8'))
