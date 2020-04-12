from django.contrib.auth.models import User, Group
from api.models import UserKey, Image
from rest_framework import serializers
from api.util import Utility
from rest_framework.request import Request

class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField()
    name = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=50, default='')
    password = serializers.CharField(max_length=50, default='', write_only=True)
    date_added = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print('serializer run')
        user = self.context['request'].user
        validated_data['owner_id'] = user.id
        password = validated_data['password']
        del validated_data['password']
        new_instance = Image.objects.create(**validated_data)
        new_instance.encrypt(password)
        new_instance.sign(user)
        new_instance.save()
        return new_instance

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
    is_active = serializers.BooleanField(default=True, read_only=True)
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
        instance.set_password(validated_data.get('password', instance.password))
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['userkey']
