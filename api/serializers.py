from django.contrib.auth.models import User, Group
from api.models import UserKey, Image
from rest_framework import serializers
from api.util import Utility
from rest_framework.request import Request

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'name', 'description', 'date_added']

    def create(self, validated_data):
        validated_data['owner_id'] = 1
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
class UserKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKey
        fields = ['private_key', 'public_key']

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    date_joined = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(default=True)
    userkey = UserKeySerializer(read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        private_key, public_key = Utility.generate_keys()
        key = UserKey(user_id=user.id, private_key=private_key, public_key=public_key)
        key.save()
        return user 
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['userkey']
