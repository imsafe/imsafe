from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import viewsets
from api.serializers import UserSerializer, UserKeySerializer, ImageSerializer
from django.http import request
from rest_framework.response import Response
from api.models import UserKey, Image, UserRelation
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
import copy

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
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def create(self, request, *args, **kwargs):
        print('create run')
        # serializer method'unu buraya tasi
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['POST'])
    def transfer(self, request, pk=None):
        user = request.user
        image = self.get_object()
        transfer_image = copy.deepcopy(image)
        transfer_image.id = None
        new_owner = User.objects.get(id=request.POST.get('new_owner'))
        transfer_image.owner = new_owner
        transfer_image.sign(new_owner)
        transfer_image.save()

        return Response({'transfer': 'ok'})

    @action(detail=True, methods=['POST'])
    def decrypt(self, request, pk=None):
        password = request.POST.get('password')
        user = request.user
        image = self.get_object()
        is_valid = image.verify(user)

        if is_valid:
            decrypted_image = image.decrypt(password)
            load = {
                'image' : decrypted_image,
                'name' : image.name,
                'description': image.description,
            }

            return Response(load)
        else:
            return Response({'error': 'signature is not valid'})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

class UserKeyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserKey.objects.all()
    serializer_class = UserKeySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
def search_user(request):
    query = request.POST.get("name")
    res = []
    if query != '':
        users = User.objects.filter(username__contains= query)
        serializer = UserSerializer(users, many=True)
        res = serializer.data
    return Response(res)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
def followings(request):
    user = request.user
    relations = UserRelation.objects.get(user=user)
    load = []
    
    for relation in relations.follows.all():
        load.append(relation.user)

    serializer = UserSerializer(load, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
def followers(request):
    relations = UserRelation.objects.filter(follows__user=request.user)
    load = []
    
    for relation in relations:
        load.append(relation.user)

    serializer = UserSerializer(load, many=True)

    return Response(serializer.data)
