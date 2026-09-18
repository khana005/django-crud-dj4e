from django.test import TestCase, Client

class PollsViewTests(TestCase):
    def test_polls_owner(self):
        client = Client()
        response = client.get('/polls/owner')
        self.assertEqual(response.status_code, 200)
        self.assertIn('53a9b4c9', response.content.decode('utf-8'))
        self.assertIn('polls owner', response.content.decode('utf-8'))
