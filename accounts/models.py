from django.db import models
from django.contrib.auth.models import User

class tokens(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=9)

    def __str__(self):
        return f"Token: {self.token}"
# Create your models here.
