from django.core.management.base import BaseCommand
from django.utils import timezone
from ... import models

from django.core.management.base import BaseCommand
from django.utils import timezone
from tokens.models import Tokens

class Command(BaseCommand):
    help = 'Delete expired tokens'

    def handle(self, *args, **options):
        current_time = timezone.now()
        fifteen_minutes_ago = current_time - timezone.timedelta(minutes=15)

        expired_tokens = Tokens.objects.filter(created_at__lte=fifteen_minutes_ago)
        num_deleted, _ = expired_tokens.delete()

        self.stdout.write(self.style.SUCCESS(f'{num_deleted} expired tokens deleted successfully'))
