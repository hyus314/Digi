from django.db import models
from django.contrib.auth.models import User
from connections.models import Connection 

# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, default=None)