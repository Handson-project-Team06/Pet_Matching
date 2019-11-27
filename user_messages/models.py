from django.db import models


class UserMessages(models.Model):
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='send_messages')
    receiver = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='receive_messages')
    pet = models.ForeignKey('matching.Pet', on_delete=models.CASCADE)
    content = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)