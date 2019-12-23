from django.shortcuts import render
from django.http import HttpResponse
from . import encrypt_img_slice as enc
from .forms import EncryptForm
from .forms import DecryptForm
from .models import Image
from senior_project.settings import MEDIA_ROOT
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your views here.

def encrypt(request):

    if request.method == 'POST':
        form = EncryptForm(request.POST)

        if form.is_valid():
            print('form posted')
        return HttpResponse(form.is_valid())
    else:
        context = {
            'form' : EncryptForm()
        }
        



    return render(request, 'senior_web/encrypt.html', {'context': context})

def decrypt(request):
    if request.method == 'POST':
        form = DecryptForm(request.POST)

        if form.is_valid():
            print('decrypt form valid')
    else:
        form = DecryptForm()
            
    return render(request, 'senior_web/decrypt.html', {'form': form})
