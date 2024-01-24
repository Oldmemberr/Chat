from rest_framework import serializers
from .models import UserInfo, Chat, Message
from djoser.serializers import TokenSerializer
from rest_framework import serializers
from djoser.conf import settings as djoser_settings
from stream_chat import StreamChat
from django.conf import settings

class StreamTokenSerializer(TokenSerializer):
    stream_token = serializers.SerializerMethodField()

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ('auth_token','stream_token')

    def get_stream_token(self, obj):
        client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)
        token = client.create_token(obj.user.id)

        return token


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