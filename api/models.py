from django.db import models
from django.contrib.auth.models import User

class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key = models.CharField(max_length=50)
    public_key = models.CharField(max_length=50)

    class Meta:
        unique_together = ['user']