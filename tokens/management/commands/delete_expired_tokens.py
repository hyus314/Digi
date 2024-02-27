from django.core.management.base import BaseCommand
from django.utils import timezone
from ... import models

class Command(BaseCommand):
    help = 'Delete expired tokens'

    def handle(self, *args, **options):
        cutoff_time = timezone.now() - timezone.timedelta(minutes=15)
        expired_tokens = models.Tokens.objects.filter(created_at__lt=cutoff_time)
        expired_tokens.delete()
        self.stdout.write(self.style.SUCCESS('Expired tokens deleted successfully'))