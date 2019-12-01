from django import forms
from matching.models import Pet


class PetCreationForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'age', 'weight', 'breed', 'picture', 'gender'\
            ,'address'
        )

    def __init__(self, user, lat, lon, *args, **kwargs):
        super(PetCreationForm, self).__init__(*args, **kwargs)
        self.user = user
        self.lat = lat
        self.lon = lon

    def save(self, commit=True):
        self.instance.owner = self.user
        self.instance.lat = self.lat
        self.instance.lon = self.lon
        return super(PetCreationForm, self).save(commit=commit)
