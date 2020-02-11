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
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from senior_web.serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def encrypt(request):

    if request.method == 'POST':
        form = EncryptForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES['image']
            fs = FileSystemStorage()
            image_filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(image_filename)
            
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            
            if password == repeat_password:
                Encryption.encrypt(password, image_filename)
                
                context = {
                    'form' : EncryptForm(),
                    'img' : image_filename
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
            public_key = request.FILES['public_key']
            signature = request.FILES['signature']

            fs = FileSystemStorage()
            public_key_filename = fs.save(public_key.name, public_key)
            signature_filename = fs.save(signature.name, signature)
            image_filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(image_filename)

            password = form.cleaned_data['password']
            
            result = Decryption.decrypt(password, image_filename, public_key_filename, signature_filename)

            if result:
                context = {
                    'form' : DecryptForm(),
                    'img' : image_filename,
                }
            else:
                context = {
                    'form' : DecryptForm(),
                    'msg' : 'The signature is not valid!'
                }
    else:
        context = {
                'form' : DecryptForm(),
            }
            
    return render(request, 'senior_web/decrypt.html', {'context': context})
