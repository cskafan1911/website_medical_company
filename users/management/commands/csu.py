import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            first_name=os.getenv('ADMIN_FIRST_NAME'),
            last_name=os.getenv('ADMIN_LAST_NAME'),
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()
