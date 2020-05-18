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
from rest_framework.permissions import AllowAny
import copy
import shutil

class ImageViewSet(viewsets.ModelViewSet):

    # TODO: refoctor class
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

    @action(detail=True, methods=['POST'])
    def transfer(self, request, pk=None):
        user = request.user
        image = self.get_object()
        transfer_image = copy.deepcopy(image)
        transfer_image.id = None
        new_owner = User.objects.get(id=request.POST.get('new_owner'))
        transfer_image.owner = new_owner
        # copy file
        new_path = ''
        path = image.image.path.split('/')
        image_name = path.pop()
        for dir in path:
            new_path += dir + '/'
        new_path += 'trn-' + str(new_owner.id) + image_name
        shutil.copy2(image.image.path, new_path)
        transfer_image.image = 'uploads/' + 'trn-' + str(new_owner.id) + image_name
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
    permission_classes_by_action = {'create': [AllowAny] }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

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
    query = request.POST.get('name')
    res = []
    if query != '':
        users = User.objects.filter(username__icontains= query)
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

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
def follow(request):
    try:
        user = request.user
        user_relation = UserRelation.objects.get(user=user)
        
        to_follow = User.objects.get(id=request.POST.get('user_id'))
        to_follow_relation = UserRelation.objects.get(user=to_follow)

        user_relation.follows.add(to_follow_relation)
        user_relation.save()
        return Response([{'follow':'true'}]) 

    except Exception:
        return Response([{'follow':'false'}]) 

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
def unfollow(request):
    try:
        user = request.user
        user_relation = UserRelation.objects.get(user=user)

        to_unfollow = User.objects.get(id=request.POST.get('user_id'))
        to_unfollow_relation = UserRelation.objects.get(user=to_unfollow)

        user_relation.follows.remove(to_unfollow_relation)
        user_relation.save()
        return Response([{'unfollow':'true'}])

    except Exception:
        return Response([{'unfollow':'false'}])