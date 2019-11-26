from django import forms
from matching.models import Pet


class PetCreationForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'age', 'weight', 'breed', 'picture', 'gender')

    def __init__(self, user, *args, **kwargs):
        super(PetCreationForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        self.instance.owner = self.user
        return super(PetCreationForm, self).save(commit=commit)
