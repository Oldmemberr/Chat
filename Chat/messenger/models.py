from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    CHAT_TYPES = (
        ('group', 'Group Chat'),
        ('private', 'Private Chat')
    )

    name = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=20, choices=CHAT_TYPES, null=True, blank=True)
    members = models.ManyToManyField(UserInfo, related_name='chats', blank=True)

    def __str__(self):
        return f'{self.name} ({self.type})'

    def get_chat_display_names(self):
        if self.type == 'group':
            if self.name:
                return f'{self.name} ({self.type})'
            else:
                return ", ".join([self.member.username for member in self.members.all()])
        elif self.type == 'private':
            members_names = [member.username for member in self.members.all()]
            return ', '.join(members_names)
        else:
            return "unknown chat"

    def get_members_display(self):
        return ", ".join([member.username for member in self.members.all()])


class Message(models.Model):
    sender = models.ForeignKey(UserInfo, related_name='sender', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE)
    content = models.TextField()
    receiver = models.ForeignKey(UserInfo, related_name='receiver', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('user_info_detail', args=[str(self.id)])

    def __str__(self):
        return self.sender.user.username if self.sender and self.sender.user else "unknown user"