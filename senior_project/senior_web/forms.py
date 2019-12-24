from django import forms
from PIL import Image
from .models import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class EncryptForm(forms.Form):
    image = forms.ImageField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

class DecryptForm(forms.Form):
    image = forms.ImageField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())