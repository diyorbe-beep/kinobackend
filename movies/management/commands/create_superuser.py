"""
Management command to create a superuser with environment variables.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **options):
        username = config('SUPERUSER_USERNAME', default='admin')
        email = config('SUPERUSER_EMAIL', default='admin@example.com')
        password = config('SUPERUSER_PASSWORD', default='admin123')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )




