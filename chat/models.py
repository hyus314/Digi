from django.db import models
from connections.models import Connection 

# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    connection_id = models.ForeignKey(Connection, on_delete=models.CASCADE)
    message = models.TextField()