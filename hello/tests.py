from django.test import TestCase, Client
import hello.urls
import hello.views

class HelloViewTests(TestCase):
    def test_hello_urls_count(self):
        # Requirement 5: hello/urls.py must contain only ONE URL entry
        self.assertEqual(len(hello.urls.urlpatterns), 1)

    def test_hello_views_count(self):
        # Requirement 6: hello/views.py must contain only ONE view for this assignment
        views_in_file = [
            attr for attr in dir(hello.views)
            if callable(getattr(hello.views, attr))
            and getattr(hello.views, attr).__module__ == 'hello.views'
        ]
        self.assertEqual(len(views_in_file), 1)

    def test_hello_session_and_cookie(self):
        client = Client()
        
        # First request
        response1 = client.get('/hello/')
        self.assertEqual(response1.status_code, 200)
        self.assertIn('view count=1', response1.content.decode('utf-8'))
        self.assertIn('53a9b4c9', response1.content.decode('utf-8'))
        
        # Check dj4e_cookie cookie
        cookie = response1.cookies.get('dj4e_cookie')
        self.assertIsNotNone(cookie)
        self.assertEqual(cookie.value, '53a9b4c9')
        self.assertEqual(cookie['max-age'], 1000)

        # Second request (session visit count incrementing)
        response2 = client.get('/hello/')
        self.assertEqual(response2.status_code, 200)
        self.assertIn('view count=2', response2.content.decode('utf-8'))

        # Third request
        response3 = client.get('/hello/')
        self.assertEqual(response3.status_code, 200)
        self.assertIn('view count=3', response3.content.decode('utf-8'))
