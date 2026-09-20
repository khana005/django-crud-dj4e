from django.test import TestCase, Client
from django.contrib.auth.models import User
from autos.models import Make, Auto

class AutosCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dj4e_user', password='Meow_3a9b4c_42')
        self.make = Make.objects.create(name='Dodge')

    def test_unauthenticated_redirect(self):
        client = Client()
        response = client.get('/autos/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_auto_list_and_meta_tags(self):
        client = Client()
        client.login(username='dj4e_user', password='Meow_3a9b4c_42')
        response = client.get('/autos/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<meta name="dj4e" content="53a9b4c9e6f79b30153c60fc0463863b">', content)
        self.assertNotIn('42-42', content)

    def test_make_delete_confirmation_button(self):
        client = Client()
        client.login(username='dj4e_user', password='Meow_3a9b4c_42')
        response = client.get(f'/autos/lookup/{self.make.id}/delete/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Yes, delete.', content)

    def test_auto_crud_lifecycle(self):
        client = Client()
        client.login(username='dj4e_user', password='Meow_3a9b4c_42')

        # Create Auto
        create_resp = client.post('/autos/main/create/', {
            'nickname': 'Speedy',
            'mileage': 55000,
            'comments': 'Great condition',
            'make': self.make.id
        })
        self.assertEqual(create_resp.status_code, 302)
        auto = Auto.objects.get(nickname='Speedy')
        self.assertEqual(auto.mileage, 55000)

        # Update Auto
        update_resp = client.post(f'/autos/main/{auto.id}/update/', {
            'nickname': 'Speedy Turbo',
            'mileage': 60000,
            'comments': 'Serviced',
            'make': self.make.id
        })
        self.assertEqual(update_resp.status_code, 302)
        auto.refresh_from_db()
        self.assertEqual(auto.nickname, 'Speedy Turbo')

        # Delete Auto GET page test
        del_get_resp = client.get(f'/autos/main/{auto.id}/delete/')
        self.assertEqual(del_get_resp.status_code, 200)
        self.assertIn('Yes, delete.', del_get_resp.content.decode('utf-8'))

        # Delete Auto POST submit
        delete_resp = client.post(f'/autos/main/{auto.id}/delete/')
        self.assertEqual(delete_resp.status_code, 302)
        self.assertFalse(Auto.objects.filter(id=auto.id).exists())

    def test_existing_polls_owner_unbroken(self):
        client = Client()
        polls_resp = client.get('/polls/owner')
        self.assertEqual(polls_resp.status_code, 200)
        self.assertIn('53a9b4c9', polls_resp.content.decode('utf-8'))
