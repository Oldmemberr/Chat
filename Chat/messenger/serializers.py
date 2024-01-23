from rest_framework import serializers
from .models import UserInfo, Chat, Message


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'user', 'avatar']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'members']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer()
    recipient = UserProfileSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'chat', 'content', 'timestamp']