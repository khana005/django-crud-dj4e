from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates or updates the dj4e_user autograder user'

    def handle(self, *args, **options):
        username = 'dj4e_user'
        password = 'Meow_3a9b4c_42'
        email = 'dj4e_user@example.com'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.email = email
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created normal user "{username}"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated normal user "{username}"'))
