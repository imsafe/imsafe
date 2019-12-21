from django.shortcuts import render
from django.http import HttpResponse
from senior_web import encrypt_img_slice as enc
# Create your views here.

def index(request):
    return render(request, 'senior_web/index.html')
