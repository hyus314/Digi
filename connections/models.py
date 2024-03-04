from django.db import models
from django.contrib.auth.models import User

class Connection(models.Model):
    id = models.AutoField(primary_key=True)
    user_one = models.ForeignKey(User, related_name='connections_one', on_delete=models.CASCADE, default=None)
    user_two = models.ForeignKey(User, related_name='connections_two', on_delete=models.CASCADE, default=None)
