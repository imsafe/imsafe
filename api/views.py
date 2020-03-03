from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import UserSerializer, UserKeySerializer, ImageSerializer
from django.http import request
from rest_framework.response import Response
from api.models import UserKey, Image

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
