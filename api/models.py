from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from api import encrypt_img_slice as encryption

class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key = models.TextField()
    public_key = models.TextField()

    class Meta:
        unique_together = ['user']

class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField(default='')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, default='')
    # hash_code = models.TextField() # Tipini belirle
    date_added = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    def encrypt(self, password):
        # enc method
        encryption.encrypt(self, password)
        pass

    def decrypt(self):
        pass

    def sign(self):
        pass

    def verify(self):
        pass

    def hash_code(self):
        pass