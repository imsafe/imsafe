from django.contrib.auth.models import User
from api.models import UserKey, Image, UserRelation
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
        user = self.context['request'].user
        password = validated_data['password']
        del validated_data['password']
        # TODO: Encrypt image before persist
        new_instance = Image.objects.create(**validated_data, owner=user)
        new_instance.encrypt(password)
        new_instance.sign(user)
        new_instance.save()
        return new_instance

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class UserKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKey
        fields = ['public_key']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    date_joined = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, default=True)
    userkey = UserKeySerializer(read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        private_key, public_key = Utility.generate_keys()
        key = UserKey(user_id=user.id)
        UserKey.objects.create(user=user, private_key=private_key, public_key=public_key)
        UserRelation.objects.create(user=user)

        return user
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'is_active', 'userkey']
