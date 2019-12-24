from django.shortcuts import render
from django.http import HttpResponse
from . import encrypt_img_slice as enc
from .forms import EncryptForm
from .forms import DecryptForm
from .models import Image
from senior_project.settings import MEDIA_ROOT
from django.core.files.uploadedfile import SimpleUploadedFile
from . import encrypt_img_slice as Encryption
from . import decrypt_img_slice as Decryption
from django.core.files.storage import FileSystemStorage
# Create your views here.

def encrypt(request):

    if request.method == 'POST':
        form = EncryptForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            
            if password == repeat_password:
                Encryption.encrypt(password, filename)
                # fotoyu bastir
                context = {
                    'form' : EncryptForm(),
                    'img' : uploaded_file_url
                }
            else:
                return HttpResponse('don\'t matched')
        else:
            return HttpResponse('not valid') 

    else:
        context = {
            'form' : EncryptForm()
        }
        
    return render(request, 'senior_web/encrypt.html', {'context': context})

def decrypt(request):
    if request.method == 'POST':
        form = DecryptForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)

            password = form.cleaned_data['password']
            
            Decryption.decrypt(password, filename)

            return HttpResponse("decrypted")
    else:
        form = DecryptForm()
            
    return render(request, 'senior_web/decrypt.html', {'form': form})
