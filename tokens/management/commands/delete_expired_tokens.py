from django.core.management.base import BaseCommand
from django.utils import timezone
from ... import models

from django.core.management.base import BaseCommand
from django.utils import timezone
from tokens.models import Tokens

class Command(BaseCommand):
    help = 'Delete expired tokens'

    def handle(self, *args, **options):
        # Get the current time
        current_time = timezone.now()

        # Iterate through each token
        for token in Tokens.objects.all():
            # Calculate the expiration time for the token using the offset
            expiration_time = token.created_at + timezone.timedelta(minutes=token.offset)
            
            # Check if 15 minutes have passed since creation based on the expiration time
            if current_time >= expiration_time + timezone.timedelta(minutes=15):
                # Delete the token
                token.delete()

        self.stdout.write(self.style.SUCCESS('Expired tokens deleted successfully'))
