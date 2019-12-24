from django.db import models
from django.conf import settings

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique = True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Image(models.Model):
    image = models.ImageField(upload_to = 'uploads', null=True, blank=True, default=None)
    # password = models.CharField(max_length=20)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)