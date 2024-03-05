from django.db import models
from django.contrib.auth.models import User

class Connection(models.Model):
    id = models.AutoField(primary_key=True)
    user_one = models.ForeignKey(User, related_name='connections_one', on_delete=models.CASCADE, default=None)
    user_two = models.ForeignKey(User, related_name='connections_two', on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        if self.user_one == self.user_two:
            raise ValueError("user_one and user_two must be different users.")
        
        # Ensure there are no duplicate connections
        if Connection.objects.filter(user_one=self.user_one, user_two=self.user_two).exists():
            raise ValueError("Connection already exists.")
        
        if Connection.objects.filter(user_one=self.user_two, user_two=self.user_one).exists():
            raise ValueError("Reverse connection already exists.")
        
        super(Connection, self).save(*args, **kwargs)