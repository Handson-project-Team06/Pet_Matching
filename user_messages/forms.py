from django.forms import models
from user_messages.models import UserMessages

class UserMessageForm(models.ModelForm):
    class Meta:
        model = UserMessages
        fields = ['content']

    def __init__(self, receiver, sender, pet, *args, **kwargs):
        self.receiver = receiver
        self.sender = sender
        self.pet = pet
        super(UserMessageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.receiver = self.receiver
        self.instance.sender = self.sender
        self.instance.pet = self.pet
        return super(UserMessageForm, self).save(commit)