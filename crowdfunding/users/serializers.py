from rest_framework import serializers
from .models import CustomUser, Message


class FollowerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
       

class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    profile_image = serializers.URLField()
    bio = serializers.CharField(max_length=200)
    banner_image = serializers.URLField()
    following = FollowerSerializer(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
        
    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

class MessageSerializer(serializers.Serializer):
    receiver = serializers.ReadOnlyField(source='CustomUser.id')
    sender = serializers.ReadOnlyField(source='CustomUser.id')
    sent_at = serializers.DateField()
    read_at = serializers.DateField()
    body = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)