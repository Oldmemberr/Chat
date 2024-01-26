from django import forms
from .models import UserInfo, Chat, Message


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)

    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'avatar']
        labels = {
            'avatar': 'Аватар',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False


class ChatForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=UserInfo.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Chat
        fields = ['name', 'members']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class GroupChatCreationForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'members']


class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(GroupMessageForm, self).__init__(*args, **kwargs)
        if 'chat' in self.fields and self.instance.chat.type == 'group':
            self.fields['recipient'].widget = forms.HiddenInput()