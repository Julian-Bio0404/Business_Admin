"""Users commands."""

# Django
from django.core.management.base import BaseCommand

# Models
from app.users.models import User


class Command(BaseCommand):
    help = 'Verify superusers.'

    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=True)
        for user in users:
            user.verified = True
            user.save()

        self.stdout.write(self.style.SUCCESS('Superusers verified.'))