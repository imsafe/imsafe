from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import UserSerializer, UserKeySerializer, ImageSerializer
from django.http import request
from rest_framework.response import Response
from api.models import UserKey, Image
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class ImageViewSet(viewsets.ModelViewSet):

    def list(self, request):
        user = request.user
        
        try:
            images = Image.objects.filter(owner=user)
            serializer = ImageSerializer(images, many=True)
            return Response(serializer.data)
        except:
            return Response()

    queryset = Image.objects
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        print('create run')
        # serializer method'unu buraya tasi
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['POST'])
    def decrypt(self, request, pk=None):
        password = request.POST.get('password')
        user = request.user
        image = self.get_object()
        serializer = ImageSerializer(image)
        is_valid = image.verify(user)

        if is_valid:
            image.decrypt(password)
            return Response({'status': 'decrypted'})
        else:
            return Response({'error': 'signature is not valid'})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserKeyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserKey.objects.all()
    serializer_class = UserKeySerializer
