from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from api import encrypt_img_slice as encryption
from api import decrypt_img_slice as decryption
from Crypto.PublicKey import RSA
from .util import Utility as Util

class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key = models.TextField()
    public_key = models.TextField()

    def set_keys(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key

    class Meta:
        unique_together = ['user']

class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, default='')
    # hash_code = models.TextField() # Tipini belirle
    signature = models.TextField(default='')
    date_added = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    def encrypt(self, password):
        encryption.encrypt(self, password)

    def decrypt(self, password):
        return decryption.decrypt(self, password)

    def sign(self, user):
        user_keys = UserKey.objects.get(user=user)
        self.signature = Util.sign_image(self.image, user_keys.private_key)
        return self.signature

    def verify(self, user):
        user_keys = UserKey.objects.get(user=user)
        return Util.verify(self.image, user_keys.public_key, self.signature)
        
    def hash_code(self):
        pass
