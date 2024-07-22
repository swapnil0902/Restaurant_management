from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Displays all fields of the User model'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        fields = User._meta.get_fields()
        for field in fields:
            self.stdout.write(f'{field.name} ({field.get_internal_type()})')