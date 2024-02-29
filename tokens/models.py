from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime, time

import secrets
import string

class Tokens(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=9)
    created_at = models.DateTimeField()
    offset = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.token:
            self.token = self.generate_unique_token()

    def __str__(self):
        return f"Token: {self.token} - Created At: {self.created_at}"

    def save(self, *args, day=None, hours=None, minutes=None, seconds=None,offset=0, **kwargs):
        if day is not None and hours is not None and minutes is not None and seconds is not None:
            current_datetime = datetime.now().replace(day=day, hour=hours, minute=minutes, second=seconds, microsecond=0)
            self.created_at = current_datetime
            self.offset = offset
    
        super().save(*args, **kwargs)
    
    def generate_unique_token(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            token = 'DG' + ''.join(secrets.choice(alphabet) for _ in range(6)) + 'X'
            if not Tokens.objects.filter(token=token).exists():
                return token

    @staticmethod
    def token_exists_for_user(user_id):
        return Tokens.objects.filter(user_id=user_id).exists()
    
    @staticmethod
    def get_token_value_for_user(user_id):
        token_instance = Tokens.objects.filter(user_id=user_id).first()
        if token_instance:
            return token_instance
        return None